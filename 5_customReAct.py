from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage,ToolMessage
from langgraph.graph.message import add_messages
from typing import Annotated, Sequence, TypedDict
from mcp_use import MCPClient, MCPAgent
from langchain_mcp_adapters.client import MultiServerMCPClient
import os
import asyncio
import json



# ✅ ASYNC ANA KOD
async def main():
     
    load_dotenv()
    llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

# Agent durumu tipi
    class AgentState(TypedDict):
          messages: Annotated[Sequence[BaseMessage], add_messages]

# MCP istemcisi başlat
    client = MultiServerMCPClient(
            {
                "search": {
                    "command": "python",
                    "args": ["6mcpserver.py"],  # MCP server scriptin adı
                    "transport": "stdio",
                },
            }
        )
    

    async def call_model(state: AgentState):
            messages = state["messages"]
            response = await model_tools.ainvoke(messages)
            return {"messages": [response]}


    def should_continue(state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return "end"
        # Otherwise if there is, we continue
        else:
            return "continue"
      
    tools = await client.get_tools()
    model_tools = llm.bind_tools(tools)
    tools_by_name = {tool.name: tool for tool in tools}    
        
    async def tool_node(state: AgentState):
        outputs = []
        for tool_call in state["messages"][-1].tool_calls:
            tool_result =  await tools_by_name[tool_call["name"]].ainvoke(tool_call["args"])
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}   

    
    

    # Agent akış grafiği oluşturuluyor
    builder = StateGraph(AgentState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", should_continue,{
        # If `tools`, then we call the tool node.
        "continue": "tools",
        # Otherwise we finish.
        "end": END,
    },)
    builder.add_edge("tools", "agent")

    graph = builder.compile()

    # Grafiği görselleştir
    try:
        png_bytes = graph.get_graph().draw_mermaid_png()
        with open("mcp.png", "wb") as f:
            f.write(png_bytes)
        print("✅ Grafik 'mcp.png' dosyasına kaydedildi!")
    except Exception as e:
        print(f"❌ Hata: {e}")
        
    ##print("🔍 tools:", tools) tool çağrılıyor mu diye kontrol ettim.
    # Örnek istek gönder
    response = await graph.ainvoke({
        "messages": [{"role": "user", "content": "search  the weather in istanbul today"}]
    })

    print("🔍 Yanıt:", response["messages"][-1].content)

   


# Ana fonksiyonu çalıştır
if __name__ == "__main__":
    asyncio.run(main())
    
"""
https://langchain-ai.github.io/langgraph/agents/mcp/#__tabbed_1_1
https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/#define-the-graph
yararlandığım kaynaklar.
"""    
