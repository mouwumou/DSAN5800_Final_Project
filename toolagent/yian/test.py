# test.py
from tool1 import parse_purchase
import os
os.environ["OPENAI_API_KEY"] = "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"

input_text = "I bought 10 lbs of bananas for 10 yuan."
result = parse_purchase({"user_input": input_text})
print("Result:", result)

# 你可以再试其它输入文本：
# input_text = "Yesterday I purchased 5 apples for 5 GBP."
# print(parse_purchase({"user_input": input_text}))
