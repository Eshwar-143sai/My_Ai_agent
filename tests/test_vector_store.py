from memory.vector_store import memorize_information, recall_information

def test_memory_schemas():
    assert callable(memorize_information)
    assert memorize_information.name == "memorize_information"
    
    assert callable(recall_information)
    assert recall_information.name == "recall_information"
