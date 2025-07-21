from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import os

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

arama = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"),verbose=True)
tools = [arama]

react_agent=create_react_agent(
    model=llm,
    tools=tools,
)
response = react_agent.invoke({"messages": [("user", "istanbulda hissedilen sıcaklık nedir?")]})
print(response["messages"][-1].content)
#burası basic chatbot react agent ile çalışıyor.