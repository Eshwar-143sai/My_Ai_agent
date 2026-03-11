import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# Phase 8 Refinement: Slack Integration (Point 7)
"""
Instructions for Local Development using Ngrok:
If you want Slack to send webhooks directly to this application instead of using SocketMode:
1. Strip out the SocketModeHandler below and use Flask/FastAPI to serve `app`.
2. Run ngrok in your terminal: `ngrok http 3000`
3. Go to api.slack.com -> Your App -> Event Subscriptions
4. Set the Request URL to `https://<your-ngrok-id>.ngrok.io/slack/events`
5. Ensure `message.channels` bot events are subscribed!
"""

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
AGENT_API_URL = "http://127.0.0.1:8000/chat"

@app.message(".*")
def handle_message(message, say):
    user_id = message.get("user")
    text = message.get("text")
    
    try:
        say(f"Processing <@{user_id}>'s request via Enterprise LangGraph...")
        
        # We pass the slack user_id sequentially to track memory
        # Update your FastAPI schema fields if ChatInput requires a specific field
        # The current API expects 'user_id' and 'message'
        payload = {
            "user_id": user_id, 
            "message": text
        }
        
        response = requests.post(AGENT_API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            say(data.get("response", "Error parsing response from backend."))
        else:
            say(f"⚠️ Agent Backend Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        say(f"❌ Failed to reach Agent API Backend: {str(e)}")

if __name__ == "__main__":
    app_token = os.environ.get("SLACK_APP_TOKEN")
    bot_token = os.environ.get("SLACK_BOT_TOKEN")
    
    if not app_token or not bot_token:
        print("ERROR: Please configured SLACK_APP_TOKEN and SLACK_BOT_TOKEN in .env")
    else:
        print("⚡️ Bolt app is starting via Socket Mode!")
        SocketModeHandler(app, app_token).start()
