劳动法知识库与 LLM 工具集
基于 OpenAI 兼容接口的 LLM 工具封装，以及《中华人民共和国劳动法》知识库数据准备。包含日志、自动重试、成本采集（token 与耗时）、多轮对话管理、调参实验与提示词工程实践。

项目结构
project1/
├── llm_utils/                  # 工具类模块
│   ├── exceptions.py           # 自定义异常
│   ├── logger.py               # 日志配置
│   ├── retry.py                # 重试装饰器
│   ├── cost_logger.py          # 成本采集装饰器（同步/异步，记录 token 和耗时到 CSV）
│   ├── llm_client.py           # 大模型调用类 LLMClient
│   └── test.py                 # 测试脚本
├── data/
│   ├── raw/                    # 原始数据
│   │   └── 劳动法.txt          # 从 docx 转换的纯文本
│   └── processed/              # 清洗后的数据
│       ├── 劳动法_cleaned.txt  # 初步清洗后的文本
│       └── articles.json       # 按条文分割的结构化数据（107 条）
├── prompts/                    # 提示词实验脚本（可选）
├── README.md
└── requirements.txt            # 依赖列表

功能特性
LLMClient：封装 OpenAI 兼容 API 调用，支持同步/异步、自动重试、日志记录、成本采集。
成本采集装饰器：自动记录每次调用的 token 消耗、耗时、成功状态到 CSV。
重试机制：指数退避，默认重试 3 次。
日志系统：同时输出到控制台和文件 app.log。
多轮对话：手动维护 messages 列表，支持截断策略。
调参实验：对比 5 组温度与 top_p 组合对输出和 token 的影响。
提示词工程：对比角色设定、CoT、Few-Shot、结构化输出 4 种策略。
劳动法数据：已清洗并分段，可用于后续知识库检索。

环境要求
Python 3.8+
openai 库

安装依赖：
pip install openai

快速开始
1. 配置 API Key
export DEEPSEEK_API_KEY="你的DeepSeek密钥"
或在代码中直接传入：
client = LLMClient(api_key="你的key", model="deepseek-chat")

2. 单轮对话
from llm_client import LLMClient

client = LLMClient()
response = client.chat([{"role": "user", "content": "你好"}])
print(response.choices[0].message.content)

3. 多轮对话
from llm_utils.llm_client import LLMClient

client = LLMClient()
messages = [{"role": "system", "content": "你是 Python 专家"}]

while True:
    user_input = input("你：")
    if user_input.lower() == "exit":
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat(messages)
    reply = response.choices[0].message.content
    print(f"助手：{reply}")
    messages.append({"role": "assistant", "content": reply})

CSV 成本记录字段
timestamp	调用时间
model	模型名称
prompt_tokens	输入 token 数
completion_tokens	输出 token 数
total_tokens	总 token 数
latency_ms	耗时（毫秒）
success	是否成功
error	错误信息

调参实验结论
temperature=0.0：输出最稳定，适合事实性问答。
temperature=1.5：输出更随机，创意性强，但可能偏离主题。
max_tokens 过小会导致 finish_reason=length 截断，需根据问题长度设置合理值。

提示词工程结论
策略	优势	适用场景
角色设定	简洁、省 token	简单问答
CoT 思维链	逻辑清晰，推理能力强	复杂问题
Few-Shot	格式可控	需要固定输出风格
结构化输出	易于程序解析	需要结构化数据返回
数据说明

核心亮点

工程化：LLM调用封装为独立工具类，支持同步/异步、自动重试（指数退避3次）、日志双输出
成本可观测：装饰器自动采集每次调用的token消耗、耗时、成功状态，写入CSV，支持成本分析
数据就绪：《劳动法》107条条文已清洗并结构化，可直接用于RAG知识库检索
实验验证：完成5组参数调优实验、4种提示词策略对比，有量化结论

原始数据来自国家法律法规数据库，已转换为纯文本并按“第X条”分段为 JSON，方便后续向量化或关键词检索。


