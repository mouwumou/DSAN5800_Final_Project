from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.tools import tool

from spending.models import Expense, Merchant, ExpenseCategory
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, timedelta
import dateparser, json

User = get_user_model()

@tool("process_receipt", return_direct=True)
def process_receipt(base64_image: str) -> str:
    """
    Processes a receipt image to identify the product, price, and merchant.
    It returns a JSON structure with `merchant`, `time`, and a `good_list` of products.
    If no time can be recognized, `time` should be an empty string.

    Parameters:
        base64_image (str): The base64 encoded image.

    Returns:
        str: The model response containing the structured JSON.
    """

    chat = ChatOpenAI(model_name="gpt-4o")

    messages = [
        HumanMessage(content="""Please help me identify the product, price, and merchant on a receipt and return it in the correct format. If the time on the receipt can be recognized, please return it together.

The desired output format:
{
    "merchant": "<merchant_name>",
    "time": "<recognized_time>",
    "good_list": [
        { "name": "<product_name>", "price": <product_price> },
        { "name": "<product_name>", "price": <product_price> }
    ]
}

If no time can be recognized, just leave "time" as an empty string."""),
        HumanMessage(content=f"Here is the image data:\ndata:image/jpeg;base64,{base64_image}")
    ]

    response = chat(messages)
    return response.content



@tool("create_or_update_expense_tool", return_direct=True)
def create_or_update_expense_tool(input_data):
    """
    Creates or updates an expense record.
    Input:
        input_data: A dictionary containing the following
        {
            "expense_id": 1,  # Optional, if provided, it will update the existing expense record
            "amount": 150.0,
            "expense_datetime": "2024-12-01T10:30:00Z",
            "user_id": 1,
            "merchant_id": 2,  # Optional
            "category_id": 3,  # Optional
            "description": "Test description" # Optional
        }
    Output:
        Returns the created or updated expense record on success, or an error message on failure.
    """
    try:
        input_data = json.loads(input_data)
        expense_id = input_data.get("expense_id")
        user_id = 1 # here we just use admin user
        user = User.objects.get(id=user_id)

        # 如果存在 expense_id，则为更新操作
        if expense_id:
            expense = Expense.objects.get(id=expense_id, user=user)
            for key, value in input_data.items():
                if hasattr(expense, key) and value is not None:
                    setattr(expense, key, value)
        else:
            # 新建操作
            input_data["expense_datetime"] = dateparser.parse(input_data["expense_datetime"])
            merchant = Merchant.objects.get(id=input_data["merchant_id"]) if input_data.get("merchant_id") else None
            category = ExpenseCategory.objects.get(id=input_data["category_id"]) if input_data.get("category_id") else None
            expense = Expense.objects.create(
                user=user,
                amount=input_data["amount"],
                expense_date=input_data["expense_datetime"],
                merchant=merchant,
                category=category,
                description=input_data.get("description", "")
            )

        expense.save()
        return {
            "success": True,
            "expense": {
                "id": expense.id,
                "amount": expense.amount,
                "expense_date": expense.expense_date.isoformat(),
                "merchant": expense.merchant.name if expense.merchant else None,
                "category": expense.category.name if expense.category else None,
                "description": expense.description,
                "created_at": expense.created_at.isoformat(),
                "updated_at": expense.updated_at.isoformat(),
            }
        }
    except ObjectDoesNotExist as e:
        return {"error": f"Object does not exist: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
    
@tool("category_tool", return_direct=True)
def category_merchant_tool(input_data):
    """
    Get the list or  specific of expense categories or merchant, or create a new one base on the input data.
    Input:
        input_data: A dictionary containing the following:
        {
            "action": "list" or "create" or "get"
            "class": "category" or "merchant"
            "category_name": "category_name" (optional, only for "create" or "get")
        }
    Output:
        Returns the list of categories, the created category, or the specific category based on the action.
    """
    input_data = json.loads(input_data) if isinstance(input_data, str) else input_data
    Model = ExpenseCategory if input_data.get("class") == "category" else Merchant
    action = input_data.get("action")
    category_name = input_data.get("category_name")
    if action == "list":
        categories = Model.objects.all()
        return [{'id': category.id, 'name': category.name} for category in categories]
    elif action == "create":
        category = Model.objects.create(name=category_name)
        return {'id': category.id, 'name': category.name}
    elif action == "get":
        try:
            category = Model.objects.get(name=category_name)
            return {'id': category.id, 'name': category.name}
        except ObjectDoesNotExist as e:
            return f"Object does not exist: {category_name}"
    else:
        return "Invalid action. Please provide 'list', 'create', or 'get'."



@tool("parse_relative_time", return_direct=True)
def parse_relative_time(natural_language_time: str):
    """
    use dateparser to parse the natural language time
    Generic parsing of relative dates like: '1 min ago', '2 weeks ago', '3 months, 1 week and 1 day ago', 'in 2 days', 'tomorrow'.
    Generic parsing of dates with time zones abbreviations or UTC offsets like: 'August 14, 2015 EST', 'July 4, 2013 PST', '21 July 2013 10:15 pm +0500'.
    Does not work with unclear datetime like "last night", "this afternoon".
    Input:
        natural_language_time: a string representing a natural language time

    Output:
        datetime object representing the parsed time
    """ 
    parsed_time = dateparser.parse(natural_language_time)
    if parsed_time:
        return parsed_time
    else:
        raise ValueError(f"无法解析时间: {natural_language_time}")
    
@tool("get_related_time", return_direct=True)
def get_related_time(input_data):
    """
    Get the datetime for a related time based on the day difference.
    If a time slot is provided, the time will be set to that time slot.
    Input:
        input_data: A dictionary containing the following:
        {
            day_diff: the difference in days from today
            time_slot (optional): the time slot in the format "HH:MM"
        }
    Output:
        datetime object representing the related time
    """
    input_data = json.loads(input_data) if isinstance(input_data, str) else input_data
    day_diff = input_data.get("day_diff", 0)
    time_slot = input_data.get("time_slot", None)
    today = datetime.now()
    related_time = today + timedelta(days=day_diff)
    if time_slot:
        time_slot = datetime.strptime(time_slot, "%H:%M")
        related_time = related_time.replace(hour=time_slot.hour, minute=time_slot.minute)
    
    # format related_time to utc format "2024-12-01T10:30:00Z"
    related_time = related_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return related_time
