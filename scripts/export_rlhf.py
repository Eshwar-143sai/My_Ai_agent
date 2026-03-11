import json
import sys

# Enterprise Phase 8: Point 10 - Fine-Tuning Prep
def extract_high_rated_interactions(database_connection=None):
    """
    In a real system, you would query PostgreSQL for queries submitted to the `/feedback` endpoint
    where `rating == 5`. Then this script formats the Request and the Agent's Response 
    into standard OpenAI JSONL format for fine-tuning a small bespoke model!
    """
    print("Gathering gold-standard RLHF conversations from database...")
    
    # Mock data that would normally be fetched from the DB
    mock_high_quality_data = [
        {"user_prompt": "What's the weather like?", "agent_response": "Searching live web... It is currently 72°F and sunny."},
        {"user_prompt": "Calculate my taxes (150 * 5).", "agent_response": "Calculated value using tools: 750."}
    ]

    count = 0
    with open("fine_tuning_dataset.jsonl", "w") as f:
        for row in mock_high_quality_data:
            # Format required by OpenAI Fine-Tuning API: {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
            entry = {
                "messages": [
                    {"role": "user", "content": row["user_prompt"]},
                    {"role": "assistant", "content": row["agent_response"]}
                ]
            }
            f.write(json.dumps(entry) + "\n")
            count += 1
            
    print(f"Generated 'fine_tuning_dataset.jsonl' with {count} perfect interactions!")
    print("You can upload this directly to OpenAI: https://platform.openai.com/finetune")

if __name__ == "__main__":
    extract_high_rated_interactions()
