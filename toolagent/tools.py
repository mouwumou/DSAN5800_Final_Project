from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import Tool
from langchain.schema import HumanMessage
from langchain.tools import tool

import base64
import json

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


# Example usage (if you just want to test the tool directly):
if __name__ == "__main__":
    import base64
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_path = "./1.jpg"

    base64_image = encode_image(image_path)
    import os
    os.environ["OPENAI_API_KEY"] = "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"

    process_receipt(base64_image)