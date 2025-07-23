Re-Act Agent 
Think : LLM kendisine verilen sorguları düşünür
Action: LLM verilen soruya karşılık cevap mı verilecek yoksa tool mu kullanılacak ona karar verir. 
Observe: Action sonunda verilen karara göre bir sonuç oluşturulur.
Bu bir döngüdür.
LangGraph ile agent workflowlarındaki döngülerde söz sahibi oluruz. 

LangGraph ile multiagent yapısı oluşturmak için birden fazla yapı var. " 4_ReAct_supervisor.py" projesinde  supervisor multiagent yapısı kullanıldı. Supervisor ajanı diğer ajanları yönetiyor.
*****
---CustomReAct projemde tool kullanımı için MCP kullandım. Lnaggraph ile MCP bağlantısı için "from langchain_mcp_adapters.client" kütüphanesini kullandım. 
--- Aynı proje içerisinde prebuilt create_react_agent yerine kendim ReAct ajanı oluşturdum. 
