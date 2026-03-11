import pytest
from tools.calculator import calculator

def test_calculator_basic_math():
    # Tools in LangChain require a dictionary matching the Pydantic schema
    result = calculator.invoke({"expression": "10 + 5"})
    assert result == "15"

def test_calculator_complex_math():
    result = calculator.invoke({"expression": "(10 * 2) / 4 + 1"})
    assert result == "6.0"

def test_calculator_invalid_math():
    result = calculator.invoke({"expression": "10 / 0"})
    # The tool returns a string starting with "Error" rather than throwing an exception
    assert "Error" in result
