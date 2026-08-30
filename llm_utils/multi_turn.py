import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),
                base_url=os.getenv("DEEPSEEK_BASE_URL")
            )

messages = [{'role': 'system','content':'你是一个善解人意的python学习助手'}]

while True:
    user_input = input('你:')
    if user_input.lower() in ('quit', 'exit'):
        break
    messages.append({'role': 'user','content': user_input})
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    reply = response.choices[0].message.content
    messages.append({'role': 'assistant', 'content': reply})
    print(f"助手：{reply}")
    print(response.usage.total_tokens,len(messages))


