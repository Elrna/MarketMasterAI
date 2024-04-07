import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def load_model(model_name="gpt2"):
    """
    指定されたモデル名でGPT-2モデルとトークナイザをロードする
    """
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    return tokenizer, model

def generate_text(prompt, tokenizer, model, max_length=50):
    """
    指定されたプロンプトに基づいてテキストを生成する
    """
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

tokenizer, model = load_model()

prompt = "Hallo:D"
generated_text = generate_text(prompt, tokenizer, model)
print(generated_text)
