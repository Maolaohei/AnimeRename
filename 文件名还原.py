import os
import csv
import argparse

def restore_filenames(csv_path):
    """
    根据CSV文件中的记录将文件名还原到原始名称。
    CSV文件应包含 'Old Path' 和 'New Path' 两列。
    """
    if not os.path.isfile(csv_path):
        print(f"CSV文件不存在: {csv_path}")
        return

    # 读取CSV文件
    with open(csv_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rename_records = list(reader)

    # 反向处理记录以避免命名冲突
    for record in reversed(rename_records):
        old_path = record['Old Path']
        new_path = record['New Path']

        if not os.path.isfile(new_path):
            print(f"跳过（新文件不存在）: '{new_path}'")
            continue

        # 确保旧路径的目录存在
        old_dir = os.path.dirname(old_path)
        if not os.path.exists(old_dir):
            try:
                os.makedirs(old_dir)
                print(f"创建目录: '{old_dir}'")
            except Exception as e:
                print(f"无法创建目录 '{old_dir}': {e}")
                continue

        try:
            os.rename(new_path, old_path)
            print(f"还原: '{new_path}' -> '{old_path}'")
        except Exception as e:
            print(f"无法还原 '{new_path}' -> '{old_path}': {e}")

def main():
    parser = argparse.ArgumentParser(description="根据CSV文件还原文件名。CSV文件应包含 'Old Path' 和 'New Path' 两列。")
    parser.add_argument('-c', '--csv', type=str, default='rename_log.csv', help='CSV文件路径，默认为当前目录下的 rename_log.csv')
    args = parser.parse_args()

    restore_filenames(args.csv)

if __name__ == "__main__":
    main()