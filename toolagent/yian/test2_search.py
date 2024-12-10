# test.py
import json
from search import process_purchase

def test_parse_purchase():
    test_cases = [
        {
            "input": "I bought 3 lbs of apples yesterday for 3 CNY.",
            "expected_keys": ["date", "item", "quantity", "price", "currency"]
        },
        {
            "input": "I bought a bag of rice today for 1000 JPY.",
            "expected_keys": ["date", "item", "quantity", "price", "currency"]
        },
        {
            "input": "I got 3 lbs of apples yesterday for 3 GBP.",
            "expected_keys": ["date", "item", "quantity", "price", "currency"]
        },
        {
            "input": "I bought apples.",
            "expected_keys": ["error"]
        },
        # 其他测试用例
        {
            "input": "I bought 2 kg of bananas tomorrow for $5.",
            "expected_keys": ["date", "item", "quantity", "price", "currency"]
        },
        {
            "input": "I bought 5 pounds of oranges for 10 EUR.",
            "expected_keys": ["date", "item", "quantity", "price", "currency"]
        },
        {
            "input": "I bought some strawberries today for 15 USD.",
            "expected_keys": ["date", "item", "quantity", "price", "currency"]
        },
        {
            "input": "I bought 1 lb of mangoes yesterday.",
            "expected_keys": ["error"]  # 缺少价格
        },
    ]

    for i, test in enumerate(test_cases):
        print(f"Test Case {i+1}:")
        user_input = test["input"]
        result = process_purchase(user_input)
        print("Input:", user_input)
        print("Output:", result)
        try:
            data = json.loads(result)
            if "error" in data:
                assert "error" in test["expected_keys"], f"Unexpected error: {data['error']}"
                print("Test Passed (Error as expected)\n")
            else:
                for key in test["expected_keys"]:
                    assert key in data, f"Missing key: {key}"
                print("Test Passed\n")
        except AssertionError as e:
            print(f"Test Failed: {e}\n")
        except json.JSONDecodeError:
            print("Test Failed: Output is not valid JSON.\n")

if __name__ == "__main__":
    test_parse_purchase()


