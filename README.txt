Re-Act Agent 
Think : LLM kendisine verilen sorguları düşünür
Action: LLM verilen soruya karşılık cevap mı verilecek yoksa tool mu kullanılacak ona karar verir. 
Observe: Action sonunda verilen karara göre bir sonuç oluşturulur.
Bu bir döngüdür.
LangGraph ile agent workflowlarındaki döngülerde söz sahibi oluruz. 

LangGraph ile multiagent yapısı oluşturmak için birden fazla yapı var. " 4_ReAct_supervisor.py" projesinde  supervisor multiagent yapısı kullanıldı. Supervisor ajanı diğer ajanları yönetiyor.

