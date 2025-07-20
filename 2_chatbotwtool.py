#burası normal basic bir chatbot. tool vs yok. langgraph dokumanından yardım alarak yapıldı.
from typing import Annotated 
from typing_extensions import TypedDict
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph , START, END
from langgraph.graph.message import add_messages
import os 
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver 
tool = TavilySearch(max_results=2)
tools = [tool]
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

class State(TypedDict): #bu sınıfta state'in ne olduğunu tanımlıyoruz. ve statelerde ne kullanılacaksa onu yazıyoruz.
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)
llm_with_tools = llm.bind_tools(tools) ##llm'in tooları kullanması için bind_tools ile bağlanıyor

def chatbot(state: State): #bu bir tool node'u. burası bir chatbot fonksiyonu. state'i alıyor ve ona göre cevap veriyor.
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot) #graphları build ettik.
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges(  #conditional edges ile tool node'u ekliyoruz. burada kullanımın kolay olması için tools_condition kullanıyoruz.bu prebuilt bir fonksiyon.
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Grafiği PNG olarak kaydetme
try:
    png_bytes = graph.get_graph().draw_mermaid_png()
    
    with open("graph.png", "wb") as f:
        f.write(png_bytes)
    
    print("✅ Grafik 'graph.png' dosyasına kaydedildi!")
    print("Dosyayı açmak için VSCode'da graph.png'ye çift tıklayın.")  
except Exception as e:
    print(f"❌ Hata: {e}")
    
# bu kod, LangGraph ile basit bir chatbot oluşturur ve kullanıcıdan gelen girdilere yanıt verir.
config = {"configurable": {"thread_id": "1"}} 
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config=config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
    except:
        print("An error occurred. Please try again.")
        break
