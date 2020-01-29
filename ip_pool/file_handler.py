import csv
import os
import random

from ip_pool import api_settings


def get_random_ip_in_pool():
    with open(api_settings.FILE_NAME, 'a+') as f:
        f.seek(0, 0)
        csv_obj = csv.reader(f)
        file_list = [item for item in csv_obj]
        addr = random.choice(file_list)[0]
    return addr


def get_ip_pool_list():
    with open(api_settings.FILE_NAME, 'a+') as f:
        f.seek(0, 0)
        csv_obj = csv.reader(f)
        file_list = [item[0] for item in csv_obj]
        return file_list


def get_last_log():
    with open(get_log_abs_path(), 'rb') as f:  # 打开文件
        off = -50  # 设置偏移量
        while True:
            try:
                f.seek(off, 2)  # seek(off, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)\
            except IOError:
                return b'0'
            lines = f.readlines()  # 读取文件指针范围内所有行
            if len(lines) >= 2:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                last_line = lines[-1]  # 取最后一行
                break
            # 如果off为50时得到的readlines只有一行内容，那么不能保证最后一行是完整的
            # 所以off翻倍重新运行，直到readlines不止一行
            off *= 2
    return last_line


def get_last_row_number():
    b_str = get_last_log().decode()
    num = b_str.split('http')[0]
    return num


def get_log_abs_path():
    if 'ip_pool' in os.path.abspath(''):
        return os.path.abspath('../log.md')
    else:
        return os.path.abspath('log.md')


def update_line_to_eof(count):
    """将指定行数文件移至末尾"""
    with open(api_settings.FILE_NAME, 'r+') as f:  # 打开文件
        cr = csv.reader(f)
        rows = [cr.__next__() for _ in range(count)]
        if not rows:
            return
        f.seek(0, 2)
        cw = csv.writer(f)
        cw.writerows(rows)
    delete_rows(1, count)


def delete_rows(del_line, count):
    """在大量数据文件下删除某几行
    del_line = 1  count = 10  删除(包括)第1行到第10行的数据
    """
    with open(api_settings.FILE_NAME, 'r') as old_file:
        with open(api_settings.FILE_NAME, 'r+') as new_file:

            current_line = 1
            # 定位到需要删除的行
            while current_line < del_line:  # (del_line - 1)
                old_file.readline()
                current_line += 1

            # 当前光标在被删除行的行首，记录该位置
            seek_point = old_file.tell()

            # 设置光标位置
            new_file.seek(seek_point, 0)

            # 读需要删除的行，光标移到下一行行首
            for _ in range(count):
                old_file.readline()

            # 被删除行的下一行读给 next_line
            next_line = old_file.readline()

            # 连续覆盖剩余行，后面所有行上移一行
            while next_line:
                new_file.write(next_line)
                next_line = old_file.readline()

            # 写完最后一行后截断文件，因为删除操作，文件整体少了一行，原文件最后一行需要去掉
            new_file.truncate()


if __name__ == '__main__':
    # update_line_to_eof(0)
    a = get_last_row_number()
    b = 1
