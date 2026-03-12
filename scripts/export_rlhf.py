import sqlite3
import json
import os

# Connect to the SQLite Database created by FastAPI
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "feedback.db")

def export_5_star_conversations():
    """
    Export all 5-star rated conversations into an OpenAI JSONL format for fine-tuning.
    """
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Query for perfect scores (RLHF positive reinforcement)
    cursor.execute("SELECT conversation_id, rating, comment FROM feedback WHERE rating = 5")
    rows = cursor.fetchall()
    
    if not rows:
        print("No 5-star ratings found yet. Keep collecting feedback!")
        return
        
    output_file = "fine_tuning_data.jsonl"
    
    # Normally you'd join this with the actual message logs from LangGraph's checkpointer
    # For this script, we'll generate the structure
    with open(output_file, 'w') as f:
        for row in rows:
            conv_id, rating, comment = row
            # Mocking the conversation extraction. In reality, query the LangGraph state.
            record = {
                "messages": [
                    {"role": "system", "content": "You are a highly capable Enterprise AI Agent."},
                    {"role": "user", "content": f"User prompt from {conv_id}"},
                    {"role": "assistant", "content": f"Ideal response associated with {conv_id}. User thought: {comment}"}
                ]
            }
            f.write(json.dumps(record) + "\n")
            
    print(f"Exported {len(rows)} 5-star conversations to {output_file} for fine-tuning.")
    conn.close()

if __name__ == "__main__":
    export_5_star_conversations()
