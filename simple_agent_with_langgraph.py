

from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from langchain_groq import ChatGroq
llm=ChatGroq(model_name="Gemma2-9b-It")

@tool
def search(query: str):
    """this is my custom tool."""
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."

search("what is a temprature in sf?")

search("what is a weather in india?")

tools=[search]

tools

tool_node=ToolNode(tools)

tool_node

llm

llm_with_tool=llm.bind_tools(tools)

llm_with_tool.invoke("hi")



"""AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_sg9d', 'function': {'arguments': '{"query":"hi"}', 'name': 'search'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 80, 'prompt_tokens': 937, 'total_tokens': 1017, 'completion_time': 0.150551835, 'prompt_time': 0.042811728, 'queue_time': 0.004417227000000003, 'total_time': 0.193363563}, 'model_name': 'Gemma2-9b-It', 'system_fingerprint': 'fp_10c08bf97d', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-cbdac5e2-5354-496c-b5ef-5d5e4faf125b-0', tool_calls=[{'name': 'search', 'args': {'query': 'hi'}, 'id': 'call_sg9d', 'type': 'tool_call'}], usage_metadata={'input_tokens': 937, 'output_tokens': 80, 'total_tokens': 1017})"""

def call_model(state: MessagesState):
    messages = state['messages']
    print(f"ye mera message hai {messages}")
    response = llm_with_tool.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal["tools", END]:
    print(f"here is a state from should continue {state}")
    messages = state['messages']
    last_message = messages[-1]
    print(f"here is a last message from should continue {last_message}")
    if last_message.tool_calls:
        return "tools"
    return END

response = llm_with_tool.invoke("hi how are you?")
state={"messages": [response]}

state={"messages": [response]}

messages = state['messages']

messages[-1]

response = llm_with_tool.invoke("what is a temprature in india?")
state={"messages": [response]}

response.tool_calls

state

should_continue(state)

print(MessagesState)

# Define a new graph
workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges("agent",should_continue,{"tools": "tools", END: END})

app = workflow.compile()

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges("agent",should_continue,{"tools": "tools", END: END})

app = workflow.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

state=app.invoke({"messages": ["what is the weather in sf"]})

state

app.invoke({"messages": ["hi how are you?"]})

call_model(state)

workflow.add_edge("tools", 'agent')

for output in app.stream(state):
    for key,value in output.items():
        print(f"here is output from {key}")
        print("_______")
        print(value)
        print("\n")

"""# now the next step"""

from langchain_community.tools.tavily_search import TavilySearchResults
tool = TavilySearchResults(max_results=2)
tools = [tool]
tool.invoke("What's a 'node' in LangGraph?")

tool_node = ToolNode(tools=[tool])

updated_llm=llm.bind_tools(tools)

updated_llm.invoke("hi")

updated_llm.invoke("hi how are you?")

def call_model(state: MessagesState):
    messages = state['messages']
    print(f"ye mera message hai from tavilay {messages}")
    response = updated_llm.invoke(messages)
    return {"messages": [response]}

def route_tools(
    state:MessagesState ,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END

# Define a new graph
workflow2 = StateGraph(MessagesState)

workflow2.add_node("agent", call_model)
workflow2.add_node("tools", tool_node)

workflow2.add_edge(START, "agent")

workflow2.add_conditional_edges("agent",route_tools,{"tools": "tools", END: END})

workflow2.add_edge("tools", 'agent')

app2 = workflow2.compile()


app2.invoke({"messages":["hi how are you?"]})

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# Define a new graph
workflow3 = StateGraph(MessagesState)

workflow3.add_node("agent", call_model)
workflow3.add_node("tools", tool_node)

workflow3.add_edge(START, "agent")

workflow3.add_conditional_edges("agent",route_tools,{"tools": "tools", END: END})

workflow3.add_edge("tools", 'agent')

app3 = workflow3.compile(checkpointer = memory)

from IPython.display import Image, display

try:
    display(Image(app3.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

config = {"configurable": {"thread_id": "1"}}

user_input = "Hi there! My name is Sunny."

events = app3.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    event["messages"][-1].pretty_print()

user_input = "can you tell me what was my name?"

# The config is the **second positional argument** to stream() or invoke()!
events = app3.stream(
    {"messages": [("user", user_input)]}, config, stream_mode="values"
)
for event in events:
    event["messages"][-1].pretty_print()

config

app3.checkpointer

memory.get(config)

