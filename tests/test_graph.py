import pytest
from core.graph import build_graph
from langchain_core.messages import HumanMessage

def test_build_graph():
    app = build_graph()
    assert app is not None

def test_graph_compile():
    app = build_graph()
    state = {"messages": [HumanMessage(content="Hello")]}
    # Just verifying the graph object can be structured
    assert hasattr(app, "invoke")
