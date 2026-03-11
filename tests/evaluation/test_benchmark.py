import pytest
from langchain_core.messages import HumanMessage
from core.graph import build_graph
from core.config import settings
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

import os
import json

# Enterprise Point 4: Evaluation Benchmarks via LLM-as-a-judge

DATA_FILE = os.path.join(os.path.dirname(__file__), "test_data.json")
with open(DATA_FILE, "r") as f:
    eval_suite = json.load(f)

class EvaluationScore(BaseModel):
    score: int = Field(description="Score from 1 to 5")
    reasoning: str = Field(description="Explanation of the score")

@pytest.fixture
def agent_graph():
    return build_graph()

@pytest.fixture
def judge_llm():
    if not settings.openai_api_key:
        pytest.skip("OpenAI API Key not set. Cannot run LLM judge.")
    # Initialize a strictly-typed judge using LangChain's structured output
    llm = ChatOpenAI(model=settings.llm_model_name, temperature=0.0)
    return llm.with_structured_output(EvaluationScore)

def evaluate_response(judge_llm, question: str, response: str, instructions: str = None) -> EvaluationScore:
    """Helper function to run the LLM judge against an agent's response."""
    base_instructions = "Evaluate the response on a scale of 1 to 5 based on accuracy and helpfulness."
    if instructions:
        base_instructions = instructions
        
    prompt = f"""
    You are an impartial, strict enterprise evaluator.
    {base_instructions}
    
    User Query: {question}
    Agent Response: {response}
    """
    return judge_llm.invoke(prompt)

@pytest.mark.parametrize("test_case", eval_suite, ids=[tc["id"] for tc in eval_suite])
def test_agent_behavior_benchmark(agent_graph, judge_llm, test_case):
    """Dynamically tests agent capabilities based on the JSON configuration."""
    question = test_case["question"]
    instructions = test_case["instructions"]
    thread_id = test_case["id"]
    
    state = {"messages": [HumanMessage(content=question)]}
    # Provide a thread_id for the MemorySaver
    result = agent_graph.invoke(state, {"configurable": {"thread_id": f"eval_{thread_id}"}})
    final_response = result["messages"][-1].content
    
    evaluation = evaluate_response(judge_llm, question, final_response, instructions)
    
    print(f"\n[{thread_id}] Eval Score: {evaluation.score}. Reasoning: {evaluation.reasoning}")
    assert evaluation.score >= 4, f"{thread_id} benchmark failed. Agent said: {final_response}"
