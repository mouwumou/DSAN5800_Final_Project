# tools_app/utils.py
from langchain.tools import Tool
from .models import Tool as ToolModel
from .models import History
from .agent_tools import my_tool_functions
from django.contrib.auth import get_user_model


User = get_user_model()

# def load_tools():
#     """Load Tool objects from the database and return a list of Tool objects."""
#     tools = []
#     for tool in ToolModel.objects.all():
#         tools.append(
#             Tool(
#                 name=tool.name,
#                 description=tool.description,
#                 func=lambda input_data, prompt=tool.prompt_template: prompt.format(data=input_data)
#             )
#         )
#     return tools

def load_tool_mappings():
    """
    动态加载工具及其后端函数
    """
    tools = Tool.objects.all()
    tool_mappings = {}
    for tool in tools:
        if tool.backend_function in my_tool_functions:
            tool_mappings[tool.name] = {
                "function": my_tool_functions[tool.backend_function],
                "description": tool.description,
                "prompt_template": tool.prompt_template
            }
    return tool_mappings

def save_or_update_session(user_id, session_id, user_input, model_response, tool_used=None):
    """
    保存或更新历史记录中的多轮交互。
    """
    try:
        # 查找是否存在当前会话
        user = User.objects.get(id=user_id)
        history = History.objects.get(user=user, session_id=session_id)
        # 更新 existing_history_data
        history_data = history.conversation
        history_data.append({
            "query": user_input,
            "response": model_response,
            # "tool_used": tool_used
        })
        history.conversation = history_data
        history.save()
    except History.DoesNotExist:
        # 如果会话不存在，创建新的会话
        history = History.objects.create(
            user=user,
            session_id=session_id,
            conversation=[{
                "query": user_input,
                "response": model_response,
                # "tool_used": tool_used
            }]
        )
        history.save()

def call_tool(tool_name, input_data, context):
    """
    动态调用指定的工具，并更新上下文
    tool_name: 工具名称
    input_data: 当前轮的输入数据
    context: 上下文，用于跨轮工具调用
    """
    tool_mappings = load_tool_mappings()
    if tool_name not in tool_mappings:
        return f"工具 {tool_name} 不存在或未启用。", context

    # 获取工具函数
    tool_function = tool_mappings[tool_name]["function"]

    # 调用工具并捕获结果
    result = tool_function(input_data)

    # 更新上下文
    context[tool_name] = result
    return result, context