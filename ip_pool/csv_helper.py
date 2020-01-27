import csv
import random

from ip_pool import api_settings


def get_random_ip_in_pool():
    with open(api_settings.FILE_NAME, 'r') as f:
        csv_obj = csv.reader(f)
        file_list = [item for item in csv_obj]
        addr = random.choice(file_list)[0]
    return addr


def get_ip_pool_list():
    with open(api_settings.FILE_NAME, 'r') as f:
        csv_obj = csv.reader(f)
        file_list = [item[0] for item in csv_obj]
        return file_list


class CsvHelper:

    @staticmethod
    def delete_row(delete_row, filename):
        ip_list = CsvHelper._get_info(filename)
        ip_list.remove(delete_row)

        CsvHelper._write_info(filename, ip_list)

    @staticmethod
    def _write_info(filename, content_list):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for row in content_list:
                writer.writerow([row])

    @staticmethod
    def _get_info(filename):
        ip_list = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for item in reader:

                try:
                    ip_list.append(item[0])
                except Exception:
                    pass
        return ip_list

    @staticmethod
    def sort_csv(filename):
        ip_list = CsvHelper._get_info(filename)
        ip_list.sort()
        CsvHelper._write_info(filename, ip_list)

    @staticmethod
    def let_no_repeat(filename):
        ip_list = CsvHelper._get_info(filename)
        for i in range(len(ip_list) - 1, -1, -1):
            if ip_list.count(ip_list[i]) > 1:
                ip_list.remove(ip_list[i])
        CsvHelper._write_info(filename, ip_list)


if __name__ == '__main__':
    c01 = CsvHelper()
    c01.let_no_repeat('proxies1.csv')
    c01.sort_csv('proxies1.csv')
    c01.delete_row('a', 'proxies1.csv')
