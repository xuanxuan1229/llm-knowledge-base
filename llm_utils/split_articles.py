from pathlib import Path
import re
import json

# 定位项目根目录
BASE_DIR = Path(__file__).parent.parent

# 清洗后文本路径
CLEANED_PATH = BASE_DIR / "data" / "processed" / "劳动法_cleaned.txt"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "articles.json"

# 读取清洗后的文本
with open(CLEANED_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 匹配“第一条”、“第二条”……“第一百二十三条”等中文数字条文标题
# 用正向前瞻，保证标题本身也被包含在片段开头
pattern = r'(?=第[一二三四五六七八九十百千万零]+条)'

# 分割文本
parts = re.split(pattern, text)

# 去掉开头可能为空的部分
articles = [part.strip() for part in parts if part.strip()]

# 保存为 JSON，每项是一个条文片段
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"共分割出 {len(articles)} 个条文片段，已保存到：{OUTPUT_PATH}")