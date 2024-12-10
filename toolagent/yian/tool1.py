# tool1.py
import os
import json
from typing import Optional, Type

from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.tools import tool
os.environ["OPENAI_API_KEY"] = "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"

class ParsePurchaseInput(BaseModel):
    user_input: str = Field(
        description="The English text describing a purchase, e.g. 'I bought 10 lbs of bananas yesterday for 30 GBP'."
    )

@tool(args_schema=ParsePurchaseInput, return_direct=True)
def parse_purchase(user_input: str) -> str:
    """
    Parse a user's purchase description in English and return a JSON with:
    - date (ISO 8601 format)
    - item (purchased item name)
    - quantity (in kilograms)
    - price (in USD)
    - currency: "USD"
    """

    system_template = """
    You are a tool that extracts structured information from a user's purchase description.

    The user provides an English sentence describing a purchase, which may include:
    - Date/time (today=2024-12-09, yesterday=2024-12-08, tomorrow=2024-12-10)
    - Item name
    - Quantity with units (convert all to kilograms; 1 lb ≈ 0.453592 kg)
    - Price and currency (convert price to USD; e.g. yuan=0.14 USD, GBP=1.25 USD, etc.)

    Instructions:
    1. Identify the date. If none given, use 2024-12-09.
    2. Identify the item.
    3. Identify quantity and convert to kg.
    4. Identify price and convert to USD.
    5. Return STRICTLY in JSON format with keys: date, item, quantity, price, currency.
    6. Do NOT include any extra text, explanation, or formatting outside the JSON. NO code blocks, NO additional text.
    7. If you cannot comply, return a JSON with an "error" key explaining the issue.

    The final answer MUST be a valid JSON object without any extra characters.
    """

    user_template = "{user_input}"

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=512)
    system_message = SystemMessagePromptTemplate.from_template(system_template)
    user_message = HumanMessagePromptTemplate.from_template(user_template)
    prompt = ChatPromptTemplate.from_messages([system_message, user_message])

    # 调用模型
    response = llm.invoke(prompt.format_prompt(user_input=user_input))
    raw_result = response.content.strip()

    print("Raw LLM Output:", raw_result)  # 调试输出

    try:
        data = json.loads(raw_result)
        required_keys = ["date", "item", "quantity", "price", "currency"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing key: {key}")
        result = json.dumps(data)
    except Exception as e:
        print("JSON parse error:", e)
        print("Raw output was:", raw_result)
        result = json.dumps({"error": "Unable to parse the output", "details": str(e)})

    return result





