import re
from typing import Union, Final

LVL: Final[list[str]] = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

def log_processing(log: str) -> dict[str, dict[str, int]]:
    dct: dict[str, dict[str, int]] = {}
    try:
        with (open(log, encoding='utf-8') as file):
            for line in file:
                if 'django.request' in line:
                    match_str: list[list[str]] = re.findall(r".+\s(\w+) django.request:?:.*?(/\S+)", line)
                    if match_str:
                        level, handler = match_str[0]
                        if handler not in dct:
                            dct[handler] = dict.fromkeys(LVL, 0)
                        dct[handler][level] += 1
    except Exception:
        raise
    return dct


def handlers_report(file_logs: list[str]) -> tuple[list[list[Union[str, int]]], str]:
    report_dict: dict[str, dict[str, int]] = {}
    for log in file_logs:
        current_dict = log_processing(log)

        # Объединение словарей с суммированием значений
        union_dict = {**report_dict, **current_dict}
        for key in report_dict.keys() & current_dict.keys():
            union_dict[key] = {l: report_dict[key][l] + current_dict[key][l] for l in LVL}
        report_dict = {**union_dict}

    # Сортировка и преобразование в список
    report_dict = dict(sorted(report_dict.items()))
    report_list: list[list[Union[str, int]]] = [
        [handler, *counts.values()]
        for handler, counts in report_dict.items()
    ]

    return [['HANDLER', *LVL], *report_list], 'requests'
