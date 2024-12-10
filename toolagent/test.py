from openai import OpenAI
import os 

import base64
os.environ["OPENAI_API_KEY"] = "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"

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "./1.jpg"

base64_image = encode_image(image_path)


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": """Please help me identify the product, price, and merchant on a receipt and return it in the correct format. If the time on the receipt can be recognized, please return it together.

    The desired output format:
    {
        "merchant": "<merchant_name>",
        "time": "<recognized_time>",
        "good_list": [
            { "name": "<product_name>", "price": <product_price> },
            { "name": "<product_name>", "price": <product_price> }
        ]
    }

    If no time can be recognized, just leave "time" as an empty string."""},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    }
                },
            ],
        }
    ],
    max_tokens=300,
)

print(response.choices[0])
