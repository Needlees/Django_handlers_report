import sys, re
from typing import Union, List, Tuple, Final

from handlers_report import handlers_report

REPORTS: Final[List[str]] = ['handlers']


def parse_args() -> Tuple[List[str], str]:
    logs: List[str] = []
    report: str = ''
    match_str: List[Tuple[str, str, str]] = re.findall(r"(.*)--report\s(\w+)(.*)", ' '.join(sys.argv[1:]))

    if match_str:
        report = match_str[0][1]
        logs_str: str = match_str[0][0] if match_str[0][0] else match_str[0][2]
        logs = logs_str.strip().split()

    return logs, report


def check_files(files: List[str]) -> bool:
    for f in files:
        try:
            with open(f, encoding='utf-8'):
                pass
        except FileNotFoundError:
            return False
    return True


def print_report(table: List[List[Union[str, int]]], total_caption: str) -> None:
    # Вычисление итогов
    total_col: List[int] = [sum(i for i in row if isinstance(i, int)) for row in table[1:]]
    total_row: List[int] = [
        sum(table[j][i] if isinstance(table[j][i], int) else 0 for j in range(1, len(table)))  # type: ignore[misc]
        for i in range(1, len(table[1]))
    ]
    total_all: int = sum(total_col)

    # Добавление столбца и строки с итогами
    table[0].append('TOTAL')
    for row in range(len(table[1:])):
        table[row + 1].append(total_col[row])
    table.append(['', *total_row, total_all])

    # Вычисление ширины столбцов
    col_widths: List[int] = [
        max(len(str(row[i])) for row in table)
        for i in range(len(table[0]))
    ]

    # Вывод шапки
    print(f"Total {total_caption}:", total_all)
    print()

    # Вывод таблицы
    for i in range(len(table)):
        for j in range(len(table[i])):
            print(str(table[i][j]), ' ' * (col_widths[j] - len(str(table[i][j]))), end='')
        print()


def main() -> None:
    file_logs, report_name = parse_args()

    if not report_name or report_name not in REPORTS:
        print("Something went wrong! Report or report name not specified.")
        return
    if not file_logs:
        print("Something went wrong! Files not specified.")
        return
    if not check_files(file_logs):
        print("One or more files not exist")
        return

    if report_name == 'handlers':
        print_report(*handlers_report(file_logs))


if __name__ == '__main__':
    main()
