import os
import re

def extract_chinese(text):
    """
    从文本中提取第一个连续的中文字符块。
    """
    chinese_blocks = re.findall(r'[\u4e00-\u9fff]+', text)
    if chinese_blocks:
        return chinese_blocks[0]
    return ''

def remove_bracketed_parts(text):
    """
    移除文本中所有方括号及其内容，并去除首尾空白字符。
    """
    cleaned_text = re.sub(r'\[.*?\]', '', text)
    return cleaned_text.strip()

def sanitize_filename(name):
    """
    移除文件名中的非法字符。
    """
    return re.sub(r'[<>:"/\\|?*]', '', name)

def main():
    current_dir = os.getcwd()
    for name in os.listdir(current_dir):
        full_path = os.path.join(current_dir, name)
        if os.path.isdir(full_path):
            chinese = extract_chinese(name)
            if chinese:
                new_name = chinese
            else:
                new_name = remove_bracketed_parts(name)
            new_name = sanitize_filename(new_name)
            if new_name and new_name != name:
                new_full_path = os.path.join(current_dir, new_name)
                if not os.path.exists(new_full_path):
                    try:
                        os.rename(full_path, new_full_path)
                        print(f"重命名: '{name}' -> '{new_name}'")
                    except Exception as e:
                        print(f"重命名失败: '{name}' -> '{new_name}' 错误: {e}")
                else:
                    print(f"目标名称已存在: '{new_name}'，跳过重命名。")
        else:
            continue

if __name__ == '__main__':
    main()