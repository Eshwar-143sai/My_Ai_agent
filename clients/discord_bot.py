import os
import requests
import discord
from dotenv import load_dotenv

load_dotenv()

# Phase 8, Point 7: External Integrations
# This script bridges Discord to our Enterprise FastAPI Agent.
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
AGENT_API_URL = "http://127.0.0.1:8000/chat"

class AgentBot(discord.Client):
    async def on_ready(self):
        print(f"=========================================")
        print(f"🤖 Connected to Discord as {self.user}!")
        print(f"=========================================")

    async def on_message(self, message):
        # Prevent the bot from talking to itself in an infinite loop
        if message.author == self.user:
            return

        # If anyone mentions the bot, process their query
        if self.user.mentioned_in(message):
            # Clean the mention string out of the query
            query = message.content.replace(f'<@{self.user.id}>', '').strip()
            
            # Show "typing" indicator on Discord while the Agent thinks
            async with message.channel.typing():
                try:
                    # Pass the discord user ID directly into our memory session system!
                    payload = {
                        "user_id": str(message.author.id), 
                        "message": query
                    }
                    response = requests.post(AGENT_API_URL, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        data = response.json()
                        await message.channel.send(data.get("response", "Error parsing agent response."))
                    else:
                        await message.channel.send(f"⚠️ Agent Backend Error: {response.status_code}")
                except Exception as e:
                    await message.channel.send(f"❌ Failed to reach Agent API Backend: {str(e)}")

if __name__ == "__main__":
    if not TOKEN or TOKEN == "your_discord_bot_token":
        print("ERROR: Please set a valid DISCORD_BOT_TOKEN in your .env file to run the Discord adapter.")
    else:
        # Requires message_content intents to read user messages
        intents = discord.Intents.default()
        intents.message_content = True 
        client = AgentBot(intents=intents)
        client.run(TOKEN)
