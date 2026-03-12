from tools.web_search import search_the_web

def test_web_search_schema():
    assert callable(search_the_web)
    assert search_the_web.name == "search_the_web"
