# Fine-Tuning Guide (RLHF)

To create a highly specialized version of your Enterprise AI Agent that mimics your best responses, you can fine-tune a smaller, cheaper LLM (e.g., `gpt-4o-mini` or `llama-3-8b`) using user feedback collected in production.

## 1. Export the Data
Whenever users submit a 5/5 rating to the `/feedback` endpoint, it indicates a high-quality human-approved interaction.

Run the extraction script to dump these interactions into the OpenAI JSONL format:
```bash
python scripts/export_rlhf.py
```

This creates a `fine_tuning_data.jsonl` file.

## 2. Train the Model
Upload the `fine_tuning_data.jsonl` file to your LLM provider's fine-tuning dashboard (e.g., OpenAI Fine-Tuning UI, or using HuggingFace AutoTrain).

## 3. Deployment
Once the model is trained, update your `.env` file to point to the new model ID:
```env
OPENAI_MODEL_NAME=ft:gpt-4o-mini:my-org:custom-agent-v1
```

The `get_llm_with_fallbacks()` manager in `core/llm_manager.py` will route all subsequent requests to your newly specialized model!
