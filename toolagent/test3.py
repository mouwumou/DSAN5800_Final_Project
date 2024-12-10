import os
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent, Tool

from tools import process_receipt

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPER_API_KEY"] = "86286c9c734de721379ec677db52ff477e4ccf97"


# llm = OpenAI(model_name="gpt-4o" ,temperature=0)
model = ChatOpenAI(model="gpt-4o")
tools = load_tools(["google-serper", "llm-math"], llm=model)
tools.append(
    Tool(
        name="process_receipt",
        func=process_receipt,
        description="Process a receipt image to extract merchant, time, and product info."
    )
)
agent = initialize_agent(tools, model, agent="zero-shot-react-description", verbose=True)


agent.invoke("What is the new building of Georgetown University? What is the name of the new building? And what is the age of the university raised to the 0.23 power?")


import base64
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "./1.jpg"

base64_image = encode_image(image_path)

agent.invoke(f"Use the process_receipt tool to process this image: {base64_image}")