import sys, re
from typing import Union, Final, Optional, Any, Callable

from handlers_report import handlers_report

REPORTS: Final[dict[str, Callable[[list[str]], tuple[list[list[Union[str, int]]], str]]]] = {
    'handlers': handlers_report
}


def parse_args() -> tuple[list[str], str | None]:
    logs: list[str] = []
    report: Optional[str] = None
    match_str: list[tuple[str, str, str]] = re.findall(r"(.*)--report\s(\w+)(.*)", ' '.join(sys.argv[1:]))

    if match_str:
        report = match_str[0][1]
        logs_str: str = match_str[0][0] or match_str[0][2]
        logs = logs_str.strip().split()

    return logs, report


def check_files(files: list[str]) -> None:
    if not files:
        raise FileNotFoundError("Something went wrong! Files not specified.")

    for f in files:
        try:
            with open(f, encoding='utf-8'):
                pass
        except FileNotFoundError:
            raise FileNotFoundError("One or more files do not exist.")


def print_report(table: list[list[Union[str, int]]], total_caption: str) -> None:
    # Вычисление итогов
    total_col: list[int] = [sum(i for i in row if isinstance(i, int)) for row in table[1:]]
    total_row: list[int] = [
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
    col_widths: list[int] = [
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


def report_generation() -> None:
    file_logs, report_name = parse_args()

    if report_name is None or report_name not in REPORTS:
        print("Something went wrong! No report or report name specified.")
        return

    check_files(file_logs)
    print_report(*REPORTS[report_name](file_logs))


if __name__ == '__main__':
    report_generation()
