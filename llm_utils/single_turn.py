import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个 Python 助手"},
        {"role": "user", "content": "解释什么是 GIL"}
    ],
    temperature=0.7,
    max_tokens=2000
)

print(response.choices[0].message.content)
print("\n--- Token 消耗 ---")
print("输入 tokens:", response.usage.prompt_tokens)
print("输出 tokens:", response.usage.completion_tokens)
print("总 tokens:", response.usage.total_tokens)
print(response.choices[0].finish_reason)
