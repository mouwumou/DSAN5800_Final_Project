# agent_app/agent_service.py
from langchain.agents import initialize_agent, Tool, load_tools
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI

from .utils import load_tool_mappings, save_or_update_session, call_tool
from .tools import process_receipt, create_or_update_expense_tool, parse_relative_time, get_related_time, category_merchant_tool
# def process_user_input(user_input):
#     # 加载工具
#     tools = load_tools()

#     # 初始化 LLM 和 Agent
#     llm = OpenAI(model="gpt-4o", temperature=0)
#     agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

#     # 使用 Agent 处理用户输入
#     response = agent.run(user_input)
#     return response


def process_user_input(user_id, session_id, user_input, context=None):
    """
    处理用户输入，支持多轮工具调用
    user_id: 当前用户ID
    session_id: 当前会话ID
    user_input: 用户的自然语言输入
    context: 上下文，用于多轮工具调用
    """
    if context is None:
        context = {}

    llm = ChatOpenAI(model="gpt-4o")

    # 加载工具
    # tool_mappings = load_tool_mappings()
    # tools = [
    #     Tool(
    #         name=name,
    #         description=tool_data["description"],
    #         func=lambda input_data, func=tool_data["function"]: func(input_data)
    #     )
    #     for name, tool_data in tool_mappings.items()
    # ]

    tools = load_tools(["google-serper", "llm-math"], llm=llm)
    tools.append(
        Tool(
            name="get_related_time",
            func=get_related_time,
            description="Get the time related to a given day difference and time slot. Input is a dict contains two variables: day_diff:-1, time_slot:'20:00'."
        )
    )
    tools.append(
        Tool(
            name="create_or_update_expense_tool",
            func=create_or_update_expense_tool,
            description="Create or update an expense record. Input vairables: expense_id, amount, merchant_id, category_id, expense_datetime, description."
        )
    )
    # tools.append(
    #     Tool(
    #         name="parse_relative_time",
    #         func=parse_relative_time,
    #         description="""Parse a relative time expression.
    #         Generic parsing of relative dates like: '1 min ago', '2 weeks ago', '3 months, 1 week and 1 day ago', 'in 2 days', 'tomorrow'.
    #         Generic parsing of dates with time zones abbreviations or UTC offsets like: 'August 14, 2015 EST', 'July 4, 2013 PST', '21 July 2013 10:15 pm +0500'.
    #         Does not work with unclear datetime like "last night", "this afternoon".
    #         """
    #     )
    # )
    tools.append(
        Tool(
            name="process_receipt",
            func=process_receipt,
            description="Process a receipt image to extract merchant, time, and product info."
        )
    )
    tools.append(
        Tool(
            name="category_merchant_tool",
            func=category_merchant_tool,
            description="Get the list or  specific of expense categories or merchant, or create a new one base on the input data. The input data is a dict contains three variables: action:'list' or 'create' or 'get', 'class': 'category' or 'merchant', category_name:'category_name' (optional, only for 'create' or 'get')."
        )
    )

    # 初始化 LLM 和 Agent
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

    # 使用 Agent 处理用户输入
    try:
        # Agent 解析用户意图并调用工具
        response = agent.invoke(user_input)

        # 检查是否有工具调用
        used_tool = getattr(agent, 'tool_name', None)
        tool_result = getattr(agent, 'tool_result', None)

        # if used_tool:
        #     # 如果调用了工具，保存结果并更新上下文
        #     result, context = call_tool(used_tool, tool_result, context)
        #     save_or_update_session(
        #         user_id=user_id,
        #         session_id=session_id,
        #         user_input=user_input,
        #         model_response=response,
        #         tool_used={"name": used_tool, "result": result}
        #     )
        # else:
        #     # 如果没有工具调用，仅保存结果
        #     save_or_update_session(
        #         user_id=user_id,
        #         session_id=session_id,
        #         user_input=user_input,
        #         model_response=response
        #     )
        save_or_update_session(
            user_id=user_id,
            session_id=session_id,
            user_input=user_input,
            model_response=response
        )

    except Exception as e:
        response = f"对不起，处理您的请求时发生错误：{str(e)}"

    return response, context