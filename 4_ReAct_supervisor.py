from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model
import os

load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

arama_ajan = TavilySearch(max_results=3)

react_agent=create_react_agent(
    model=llm,
    tools=[arama_ajan],
    prompt=(
        "You are a research agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with research-related tasks, DO NOT do any math\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="research_agent",
)


@tool 
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

mat_agent = create_react_agent(
    model=llm,
    tools=[multiply, add],
    prompt=(
        "You are a math agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with math-related tasks, DO NOT do any research\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="math_agent",
)


supervisor = create_supervisor(
    model=init_chat_model( model="llama-3.3-70b-versatile",
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")),
    agents=[react_agent, mat_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a research agent. Assign research-related tasks to this agent\n"
        "- a math agent. Assign math-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()

response = supervisor.invoke({"messages": [("user", "what is the age of barack obama")],})
print(response["messages"][-1].content)
# print(response)

try:
    png_bytes = supervisor.get_graph().draw_mermaid_png()
    with open("graph2.png", "wb") as f:
        f.write(png_bytes)

    print("✅ Grafik 'graph2.png' dosyasına kaydedildi!")
    print("Dosyayı açmak için VSCode'da graph2.png'ye çift tıklayın.")

except Exception as e:
    print(f"❌ Hata: {e}") 
    
    
    
"""
  supervisor multiagent kullanıldığında, supervisor diğer ajanları yönlendirmiş oluyor.bir arama yapılcağı zaman research agent devreye giriyor, 
  bir matematik işlemi yapılacağı zaman math agent devreye giriyor. supervisor, hangi ajanı çağıracağını belirliyor ve bu ajanlar kendi görevlerini yerine getiriyor.
  supervisor, her iki ajanı da yönlendirebiliyor. kendimiz node oluşturmadan langgraphın prebuilt fonksiyonlarını kullanarak bu yapıyı oluşturabiliyoruz.
"""  