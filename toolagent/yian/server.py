# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from tool1 import parse_purchase

app = Flask(__name__)
CORS(app)

# 内存中的账单数据列表
ledger_data = []

@app.route('/api/parse_purchase', methods=['POST'])
def parse_purchase_api():
    user_input = request.json.get('user_input', '')
    # 关键修改：使用字典形式传参，而不是 user_input=user_input
    result = parse_purchase({"user_input": user_input})
    data = json.loads(result)
    return jsonify(data)

@app.route('/api/save_ledger_entry', methods=['POST'])
def save_ledger_entry():
    entry = request.json
    # entry 应该包含 date, item, quantity, price, currency 字段
    if all(k in entry for k in ['date', 'item', 'quantity', 'price', 'currency']):
        ledger_data.append(entry)
        return jsonify({"status": "ok"})
    else:
        return jsonify({"error": "Incomplete entry"}), 400

@app.route('/api/ledger', methods=['GET'])
def get_ledger():
    return jsonify(ledger_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

