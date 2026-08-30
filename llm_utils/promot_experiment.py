from llm_client import LLMClient

client = LLMClient(model="deepseek-chat")

question = "什么是 Python 的 GIL？它如何影响多线程性能？"

prompts = {
    "角色设定": [
        {"role": "system", "content": "你是一位资深 Python 架构师，请用简洁的语言回答问题。"},
        {"role": "user", "content": question}
    ],
    "CoT 思维链": [
        {"role": "user", "content": f"请一步一步思考，然后回答：{question}"}
    ],
    "Few-Shot": [
        {"role": "user", "content": f"示例1：\n问题：什么是装饰器？\n回答：装饰器是一种用于修改函数行为的高级函数，它接受一个函数作为参数并返回新函数。\n\n示例2：\n问题：什么是 GIL？\n回答：GIL 是全局解释器锁，是 CPython 中的一种互斥锁，用于保证同一时刻只有一个线程执行字节码。\n\n现在回答：{question}"}
    ],
    "结构化输出": [
        {"role": "user", "content": f"请以 JSON 格式输出，包含以下字段：定义、影响、解决方案。\n问题：{question}"}
    ],
}

for name, messages in prompts.items():
    print(f"\n===== {name} =====")
    response = client.chat(messages, temperature=0.3, max_tokens=500)
    print(response.choices[0].message.content)
    print(f"总 token: {response.usage.total_tokens}")
    print(f"finish_reason: {response.choices[0].finish_reason}")