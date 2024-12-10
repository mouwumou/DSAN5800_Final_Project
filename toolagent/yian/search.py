# search.py
import os
import json
from typing import Optional

from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from datetime import datetime, timedelta
import re

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取 API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")
print(f"SERPAPI_API_KEY: {SERPAPI_API_KEY}")

class ParsePurchaseInput(BaseModel):
    user_input: str = Field(
        description="The English text describing a purchase."
    )
    resolved_date: str = Field(
        description="The resolved date in YYYY-MM-DD format."
    )
    exchange_rate_info: str = Field(
        description="Exchange rate information (e.g., '1 GBP = 1.25 USD')."
    )

@tool(args_schema=ParsePurchaseInput, return_direct=True)
def parse_purchase(user_input: str, resolved_date: str, exchange_rate_info: str) -> str:
    """
    Given a fully resolved description of a purchase:
    - `resolved_date` (YYYY-MM-DD)
    - `exchange_rate_info` (e.g. "1 GBP = 1.25 USD")
    - A sentence that includes item, quantity with units, price, etc.

    Produce a JSON with:
    {
      "date": "YYYY-MM-DD",
      "item": "<string>",
      "quantity": <number in kg>,
      "price": <number in USD>,
      "currency": "USD"
    }

    If not possible, return a JSON with an "error" key.
    """
    system_template = """
    You are a tool that extracts structured information from a user's purchase description.
    
    The user provides an English sentence describing a purchase, which may include:
    - Date (already resolved and given)
    - Item name
    - Quantity with units (convert all to kilograms; 1 lb ≈ 0.453592 kg)
    - Price and currency (convert price to USD using the provided exchange rate if not already in USD)

    Instructions:
    1. The date has been pre-resolved for you and is: {resolved_date}
    2. The exchange rate information:
       {exchange_rate_info}
       If the currency is not USD, use the provided exchange rate to convert to USD.
    3. Identify the item.
    4. Identify quantity and convert to kg.
    5. Identify price and convert to USD if needed.
    6. Return STRICTLY in JSON format with keys: date, item, quantity, price, currency.
    7. Do NOT include extra text or explanation outside the JSON. NO code blocks.
    8. If you cannot comply, return a JSON with an "error" key.
    """

    user_template = "{user_input}"

    # 初始化 LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=512)
    
    # 创建消息模板
    system_message = SystemMessagePromptTemplate.from_template(system_template)
    user_message = HumanMessagePromptTemplate.from_template(user_template)
    prompt = ChatPromptTemplate.from_messages([system_message, user_message])

    # 调用 LLM
    response = llm.invoke(
        prompt.format_prompt(
            user_input=user_input, 
            resolved_date=resolved_date, 
            exchange_rate_info=exchange_rate_info
        )
    )
    raw_result = response.content.strip()
    print(f"LLM Raw Result: {raw_result}")  # 调试信息

    try:
        data = json.loads(raw_result)
        required_keys = ["date", "item", "quantity", "price", "currency"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing key: {key}")
        result = json.dumps(data)
    except Exception as e:
        result = json.dumps({"error": "Unable to parse the output", "details": str(e)})

    return result

def get_exchange_rate(currency: str) -> Optional[float]:
    """Use SerpAPI to find the exchange rate from the given currency to USD."""
    try:
        search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
        query = f"1 {currency} to USD"
        results = search.run(query)
        print(f"SerpAPI Results for '{query}': {results}")  # 调试信息

        # 更新后的正则表达式
        match = re.search(r"^([\d,.]+)\s+(?:USD|United\s+States\s+Dollar)", results, re.IGNORECASE)
        if match:
            rate_str = match.group(1).replace(',', '')
            rate = float(rate_str)
            print(f"Exchange rate fetched: 1 {currency} = {rate} USD")  # 调试信息
            return rate
        else:
            print(f"Unable to find exchange rate for {currency} in search results.")  # 调试信息
            return None
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def get_current_date() -> str:
    """Use SerpAPI to get today's date, or fallback to local time."""
    try:
        search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY)
        results = search.run("What is today's date?")
        print(f"SerpAPI Results for 'What is today's date?': {results}")  # 调试信息
        match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}", results)
        if match:
            found_date_str = match.group(0)
            date_obj = datetime.strptime(found_date_str, "%B %d, %Y")
            print(f"Current date fetched from SerpAPI: {found_date_str}")  # 调试信息
            return date_obj.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error fetching current date: {e}")
    return datetime.now().strftime("%Y-%m-%d")

def resolve_date_if_relative(user_input: str, current_date: str) -> str:
    """Parse relative dates (yesterday, today, tomorrow) and return the resolved date."""
    date_mentioned = None
    if "yesterday" in user_input.lower():
        date_mentioned = "yesterday"
    elif "today" in user_input.lower():
        date_mentioned = "today"
    elif "tomorrow" in user_input.lower():
        date_mentioned = "tomorrow"

    date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    if date_mentioned == "yesterday":
        new_date_obj = date_obj - timedelta(days=1)
        return new_date_obj.strftime("%Y-%m-%d")
    elif date_mentioned == "tomorrow":
        new_date_obj = date_obj + timedelta(days=1)
        return new_date_obj.strftime("%Y-%m-%d")
    elif date_mentioned == "today":
        return current_date

    # If no relative date mentioned, just use current_date as default
    return current_date

def extract_currency(user_input: str) -> Optional[str]:
    """Extract currency from user input."""
    currency_pattern = r"\b(GBP|EUR|JPY|CNY|yuan|pounds?|yen|euro|\$|gbp|usd)\b"
    curr_match = re.search(currency_pattern, user_input, re.IGNORECASE)
    if curr_match:
        currency_found = curr_match.group(1).upper()
        # Normalize some variants
        if currency_found in ["YUAN"]:
            currency_found = "CNY"
        elif currency_found in ["POUNDS", "POUND"]:
            currency_found = "GBP"
        elif currency_found == "$":
            currency_found = "USD"
        return currency_found
    return None

def process_purchase(user_input: str) -> str:
    """
    Process the raw user input and return the structured JSON.
    """
    gathered_info = {}
    all_fields = ["date", "item", "quantity", "price"]

    # 获取当前日期
    current_date = get_current_date()
    # 解析相对日期
    final_date = resolve_date_if_relative(user_input, current_date)
    gathered_info["date"] = final_date

    # 提取货币
    currency_found = extract_currency(user_input)

    # 提取数量（如 "3 lbs", "2 kg"）
    qty_match = re.search(r"(\d+(?:\.\d+)?)\s*(lbs?|kg|kilograms?)", user_input, re.IGNORECASE)
    if qty_match:
        qty_val = float(qty_match.group(1))
        unit = qty_match.group(2).lower()
        if unit.startswith("lb"):
            # 转换为公斤
            qty_val = qty_val * 0.453592
        gathered_info["quantity"] = round(qty_val, 6)  # 保留六位小数

    # 提取价格（如 "for 30 GBP", "for $20"）
    price_match = re.search(r"for\s+(\d+(?:\.\d+)?)\s*(USD|GBP|EUR|JPY|CNY|\$)?", user_input, re.IGNORECASE)
    if price_match:
        price_val = float(price_match.group(1))
        currency = price_match.group(2)
        if currency:
            if currency == "$":
                currency = "USD"
            gathered_info["price"] = price_val
            if not currency_found:
                currency_found = currency.upper()
        else:
            # 如果没有指定货币，默认为USD
            gathered_info["price"] = price_val
            currency_found = "USD"

    # 提取商品名称（如 "bought apples", "got oranges"）
    item_match = re.search(r"(?:bought|got)\s+(?:some\s+)?(?:\d+\s*\w+\s+of\s+)?(\w+)", user_input, re.IGNORECASE)
    if item_match:
        item_val = item_match.group(1)
        gathered_info["item"] = item_val.lower()

    # 获取汇率信息
    if currency_found and currency_found != "USD":
        rate = get_exchange_rate(currency_found)
        if rate is None:
            # 如果无法获取汇率，返回错误
            return json.dumps({"error": f"Unable to fetch exchange rate for {currency_found}."})
        exchange_rate_info = f"1 {currency_found} = {rate} USD"
    else:
        exchange_rate_info = "No currency exchange needed or already in USD."

    # 如果已知价格但未指定货币，假设为USD
    if "price" in gathered_info and not currency_found:
        currency_found = "USD"

    gathered_info["currency"] = currency_found if currency_found else "USD"

    # 检查是否所有必要字段都已收集
    if all(field in gathered_info for field in all_fields) and "currency" in gathered_info:
        final_sentence = f"I bought {gathered_info['quantity']} kg of {gathered_info['item']} on {gathered_info['date']} for {gathered_info['price']} {gathered_info['currency']}."
        print(f"Final Sentence Sent to parse_purchase: {final_sentence}")  # 调试信息
        # 使用 invoke 方法传递参数
        result = parse_purchase.invoke({
            "user_input": final_sentence,
            "resolved_date": gathered_info["date"],
            "exchange_rate_info": exchange_rate_info
        })
        print(f"Raw parse_purchase response: {result}")  # 调试信息
        return result
    else:
        # 如果缺少字段，返回错误信息
        missing = [f for f in all_fields if f not in gathered_info or gathered_info[f] is None]
        return json.dumps({"error": f"Missing fields: {', '.join(missing)}"})

if __name__ == "__main__":
    # 示例用法
    user_input = "I bought 3 lbs of apples yesterday for 3 CNY."
    result = process_purchase(user_input)
    print("Final Result:", result)

