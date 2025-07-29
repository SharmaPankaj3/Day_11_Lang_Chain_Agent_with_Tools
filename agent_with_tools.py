from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
#from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
import math
import os
import re
# Define a simple calculator Tool:
def custom_calculator(query:str) -> str:
    try:
        query = query.lower()
        query = query.replace("divided by","/").replace("times","*").replace("plus","+").replace("minus","-")
        query = re.sub(r"[^\d\.\+\-\*\/\(\)]","",query)
        result = eval(query)
        return f"The answer is :{result}"
    except Exception as e:
        return f"Sorry, I could't calculate that.({str(e)})"

calculator_tool = Tool(
    name= "Calculator",
    func=custom_calculator,
    description= "Useful for doing math calculations.Input should be a search query"
)

# Step 2. Load API key
with open(r"D:\desktop\Key_GEN_AI.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read().strip()

# 2. Define a fake search tool
def fake_search_tool(query: str) -> str:
    # Simulate search response
    query = query.lower()
    if "paris" in query and "weather" in query:
        return "The current weather in Paris is 24°C,sunny"
    elif "capital of the france" in query:
        return "The capital of the France is paris"
    elif "population" in query and "new york" in query:
        return "The population of New York City is approximately 8.4 millions."
    elif "meters in kilometer" in query:
        return "There are 1000 meters  in a kilometers."
    elif "ounces in a pound" in query:
        return "There are 16 ounces in a pound."
    else:
        return "No results found."

search_tool= Tool(
    name="Search",
    func=fake_search_tool,
    description="Useful for searching the internet.Input should be a search query "
)

# 3. LLM Setup

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# 4  Initialize the agent
tools = [calculator_tool, search_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 5 Run the Agent
query = "What's 1212 divided by 4,then tell me What is the Paris Weather Today?"
response = agent.invoke({"input": query})
print("\nFinal Answer:\n",response)