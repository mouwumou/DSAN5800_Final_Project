# tool.py
import datetime

class NLPTool:
    """
    自然语言处理工具，用于从用户输入的自然语言中提取关键信息。
    在实际使用中可以整合NLP模型，如Rasa, spaCy, Duckling等。
    """
    def parse_user_input(self, user_input: str) -> dict:
        """
        解析用户输入内容，从中提取日期、物品、数量、价格等信息。
        返回字典格式，如:
        {
            "date": "2024-12-09",
            "item": "苹果",
            "quantity": 5,
            "unit": "斤",
            "price": None
        }
        price为None表示还未获取价格信息，需要后续对话澄清。
        """
        # 简单的示例实现（仅演示用途，不具备真实NLP能力）
        # 实际中需要使用正则/NLP模型等手段进行更智能的解析
        info = {
            "date": None,
            "item": None,
            "quantity": None,
            "unit": None,
            "price": None
        }
        
        # 假设当用户说 "今天买了5斤苹果"
        # 我们简单匹配“斤”前面的数字和“苹果”等关键词
        if "苹果" in user_input:
            info["item"] = "苹果"
        # 提取数量(假定一句话里有数字, 且紧跟单位斤)
        # 这里只是一个简单演示
        import re
        qty_match = re.search(r'(\d+)\s*斤', user_input)
        if qty_match:
            info["quantity"] = int(qty_match.group(1))
            info["unit"] = "斤"
        
        # 提取日期(假设用户说了“今天”就认为是当前日期)
        if "今天" in user_input:
            info["date"] = datetime.date.today().isoformat()

        return info


class DateTool:
    """
    日期工具，用于获取特定日期信息或进行日期解析与转换。
    """
    def get_current_date(self) -> str:
        return datetime.date.today().isoformat()
    
    def parse_date(self, text: str) -> str:
        # 这里简单假设如果文本中有“明天”就返回明天的日期，否则今天
        if "明天" in text:
            return (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        return datetime.date.today().isoformat()


class CurrencyTool:
    """
    货币工具，用于货币转换或简单的价格校验。
    """
    def convert_price(self, amount: float, from_currency: str, to_currency: str) -> float:
        # 简化处理，假设汇率1:1，仅作示例
        return amount
    
    def validate_price_format(self, price_str: str) -> float:
        # 尝试从字符串中提取float数值
        try:
            return float(price_str)
        except:
            return None


class UnitConversionTool:
    """
    单位换算工具：如从斤到千克。
    """
    def convert_unit(self, quantity: float, from_unit: str, to_unit: str) -> float:
        # 假设 1斤 = 0.5公斤
        if from_unit == "斤" and to_unit == "公斤":
            return quantity * 0.5
        return quantity


class DatabaseTool:
    """
    数据库工具，用于将最终确认的账单信息存入数据库，并查询历史记录。
    实际中需要实现连接数据库、创建表、插入数据、查询数据逻辑。
    """
    def __init__(self):
        # 假设使用内存字典作为存储，仅做演示
        self.storage = []
    
    def insert_record(self, date: str, item: str, quantity: float, unit: str, price: float, currency: str = "CNY"):
        record = {
            "date": date,
            "item": item,
            "quantity": quantity,
            "unit": unit,
            "price": price,
            "currency": currency
        }
        self.storage.append(record)
        return True

    def get_records(self):
        return self.storage


class DialogueContextTool:
    """
    对话上下文工具：用于在多轮对话中存储当前会话状态、临时信息等。
    实际中可使用数据库或Redis进行持久化，这里仅用内存字典演示。
    """
    def __init__(self):
        self.context = {}

    def set_context(self, user_id: str, key: str, value):
        if user_id not in self.context:
            self.context[user_id] = {}
        self.context[user_id][key] = value

    def get_context(self, user_id: str, key: str):
        if user_id in self.context and key in self.context[user_id]:
            return self.context[user_id][key]
        return None

    def clear_context(self, user_id: str):
        if user_id in self.context:
            self.context[user_id] = {}

