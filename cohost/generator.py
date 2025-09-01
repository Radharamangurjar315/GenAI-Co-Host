# cohost/generator.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Choose model: 'microsoft/DialoGPT-medium' (good), or 'distilgpt2' (smaller)
MODEL_NAME = "distilgpt2"  

# Load once
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).eval()

# Keep per-session chat history (you'll manage from app)
def generate_with_history(chat_history_ids, user_input, max_new_tokens=120, do_sample=True):
    """
    chat_history_ids: previous token ids tensor or None
    user_input: raw user string
    Returns: new_chat_history_ids, reply_text
    """
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    # generation - tune parameters for podcast style
    new_chat_history_ids = model.generate(
        bot_input_ids,
        max_length=bot_input_ids.shape[-1] + max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=do_sample,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
        no_repeat_ngram_size=3,
    )

    # decode only new tokens
    reply = tokenizer.decode(new_chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True).strip()
    return new_chat_history_ids, reply
