from locust import HttpUser, task, between

class AIPerformanceTest(HttpUser):
    wait_time = between(1, 4)
    
    @task
    def chat_standard(self):
        self.client.post("/chat", json={
            "user_id": "locust_tester",
            "message": "Hello, how are you? Can you tell me a short joke?"
        })
        
    @task(2)
    def test_root(self):
        self.client.get("/")
