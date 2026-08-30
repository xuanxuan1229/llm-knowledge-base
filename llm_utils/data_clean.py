# clean_text.py
with open("../data/raw/劳动法.txt", "r", encoding="utf-8") as f:
    raw = f.read()

# 1. 删除连续空行
import re
cleaned = re.sub(r'\n\s*\n', '\n', raw)

# 2. 去除每行首尾空白
cleaned = "\n".join(line.strip() for line in cleaned.splitlines() if line.strip())

# 3. 可选：去除页码（简单示例，按需修改）
cleaned = re.sub(r'\n第\s*\d+\s*页\s*共\s*\d+\s*页', '', cleaned)

with open("../data/processed/劳动法_cleaned.txt", "w", encoding="utf-8") as f:
    f.write(cleaned)

print("清洗完成，已保存为 劳动法_cleaned.txt")