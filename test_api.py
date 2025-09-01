from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "distilgpt2"   # keeping same model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Persona style prompt
persona = (
    "You are a friendly and engaging podcast co-host. "
    "Reply casually in 2-3 sentences, add a follow-up question to keep the conversation going.\n"
)

# User input
user_input = "Hello bhai"

# Prepare input
prompt = persona + "Human: " + user_input + "\nCo-Host:"
inputs = tokenizer.encode(prompt, return_tensors="pt")

# Generate with tuned parameters
outputs = model.generate(
    inputs,
    max_length=120,
    do_sample=True,
    top_k=50,
    top_p=0.92,
    temperature=0.8,
    no_repeat_ngram_size=3
)

# Decode response
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("🤖 Co-Host:", response.replace(prompt, "").strip())
