import os
import re
import argparse
import csv


def get_season_episode_from_filename(filename):
    """
    从文件名中提取季数和集数。
    支持的格式包括 'S2 - 13', 'S02E13', 'S2E13' 等。
    如果无法提取，则返回默认季数和集数。
    """
    # 定义多个正则表达式模式以匹配不同的格式
    patterns = [
        re.compile(r'S(\d+)\s*[-_]\s*(\d+)', re.IGNORECASE),  # S2 - 13 或 S2_13
        re.compile(r'S(\d+)E(\d+)', re.IGNORECASE),  # S02E13
        re.compile(r'S(\d+)E(\d+)', re.IGNORECASE),  # S2E13
    ]

    for pattern in patterns:
        match = pattern.search(filename)
        if match:
            season_num = int(match.group(1))
            episode_num = int(match.group(2))
            return season_num, episode_num
    return None, None  # 无法提取


def rename_files_in_directory(directory, rename_log):
    """
    重命名指定目录下的所有符合格式的文件，格式为 '标题 SxxExx'。
    并将重命名信息记录到 rename_log 列表中。
    """
    # 定义正则表达式模式，提取标题
    pattern = re.compile(r'^\[.*?\]\s*(.*?)\s*(S\d+\s*[-_]\s*\d+|S\d+E\d+).*?$')

    # 获取指定目录下的所有文件
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print(f"目录不存在: {directory}")
        return

    for filename in files:
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            match = pattern.match(filename)
            if match:
                # 提取主标题
                title = match.group(1).strip()

                # 提取季数和集数
                season_num, episode_num = get_season_episode_from_filename(filename)

                if season_num is None or episode_num is None:
                    print(f"无法提取季数或集数，使用默认季数 S01: '{filepath}'")
                    season_num = 1
                    # 尝试提取集数
                    episode_match = re.search(r'\[(\d{1,2})\]', filename)
                    if episode_match:
                        episode_num = int(episode_match.group(1))
                    else:
                        print(f"无法提取集数，跳过文件: '{filepath}'")
                        continue

                # 构建新的文件名
                new_filename = f"{title} S{season_num:02d}E{episode_num:02d}"

                # 保留文件扩展名
                _, ext = os.path.splitext(filename)
                new_filename_with_ext = new_filename + ext

                # 构建新的文件路径
                new_filepath = os.path.join(directory, new_filename_with_ext)

                try:
                    os.rename(filepath, new_filepath)
                    print(f"重命名: '{filepath}' -> '{new_filepath}'")
                    # 记录重命名信息
                    rename_log.append({'Old Path': filepath, 'New Path': new_filepath})
                except Exception as e:
                    print(f"无法重命名 '{filepath}': {e}")
            else:
                print(f"跳过（不匹配的文件名）: '{filepath}'")


def process_directory(root_dir, rename_log):
    """
    遍历根目录及其子目录，重命名文件。
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f"处理目录: '{dirpath}'")
        rename_files_in_directory(dirpath, rename_log)


def write_csv(rename_log, csv_path):
    """
    将重命名日志写入 CSV 文件。
    """
    # 定义 CSV 的表头
    fieldnames = ['Old Path', 'New Path']

    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in rename_log:
                writer.writerow({'Old Path': log['Old Path'], 'New Path': log['New Path']})
        print(f"重命名记录已保存到 '{csv_path}'")
    except Exception as e:
        print(f"无法写入 CSV 文件 '{csv_path}': {e}")


def main():
    parser = argparse.ArgumentParser(
        description="批量重命名文件名为格式 '标题 SxxExx'，支持递归遍历子目录，并生成重命名对照的 CSV 文件。")
    parser.add_argument('-d', '--directory', type=str, default='.', help='要处理的根目录，默认为当前目录')
    parser.add_argument('-o', '--output', type=str, default='rename_log.csv',
                        help='输出的 CSV 文件名，默认为当前目录下的 rename_log.csv')
    args = parser.parse_args()

    rename_log = []  # 用于记录所有重命名操作

    # 获取当前脚本运行的目录，以确保输出 CSV 在当前路径
    current_working_directory = os.getcwd()
    csv_output_path = os.path.join(current_working_directory, args.output)

    # 处理目录
    process_directory(args.directory, rename_log)

    # 写入 CSV 文件
    write_csv(rename_log, csv_output_path)


if __name__ == "__main__":
    main()