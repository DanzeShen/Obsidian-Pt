import os
import re

def process_md_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    skip_mode = False
    # 正则：### 后面包含【为什么重】 / 【你的进度】
    target_patterns = [
        re.compile(r"^###\s.*为什么重"),
        re.compile(r"^###\s.*你的进度")
    ]

    for line in lines:
        # 判断是否是任意级别markdown标题 # ~ ######
        is_heading = re.match(r"^#{1,6}\s", line)

        if skip_mode:
            if is_heading:
                # 遇到新标题，停止跳过，保留这个标题行
                skip_mode = False
                new_lines.append(line)
            continue

        # 检查当前行是否命中目标标题
        hit = any(pat.match(line) for pat in target_patterns)
        if hit:
            skip_mode = True
            continue  # 本行（### xxx）直接丢弃
        new_lines.append(line)

    # 写回文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"✅ 处理完成: {file_path}")


if __name__ == "__main__":
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        if filename.lower().endswith(".md") and os.path.isfile(filename):
            full_path = os.path.join(current_dir, filename)
            process_md_file(full_path)
    print("\n🎉 全部md处理完毕")
