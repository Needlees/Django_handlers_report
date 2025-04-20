import pytest
from contextlib import nullcontext as does_not_raise

from src.main import check_files, print_report, parse_args, report_generation


class TestMain:
    @pytest.mark.parametrize(
        "files, expectation",
        [
            ([r'Logs\app1.log', r'Logs\app2.log', r'Logs\app3.log'], does_not_raise()),
            ([r'Logs\app1.log'], does_not_raise()),
            ('111', pytest.raises(FileNotFoundError)),
            ([], pytest.raises(FileNotFoundError)),
        ]
    )
    def test_check_files(self, files, expectation):
        with expectation:
            check_files(files)

    @pytest.mark.parametrize(
        "table, total_caption, expectation",
        [
            ([['NAME', 'COL1', 'COL2'], ['Name1', 5, 7], ['Name2', 0, 3]], 'requests', does_not_raise()),
            ([['NAME', 'COL1', 'COL2'], ['Name1', 5, 'type1'], ['Name2', 0, 'type2']], 'logs', does_not_raise()),
            ([['NAME', 'COL1', 'COL2'], ['Name1', 5, 'type1', 12], ['Name2', 0, 'type2', 12]], 'files',
             pytest.raises(IndexError)),
        ]
    )
    def test_print_report(self, table, total_caption, expectation):
        with expectation:
            print_report(table, total_caption)

    @pytest.mark.parametrize(
        "argv, res",
        [
            (
                    ["main.py", r"Logs\app1.log Logs\app2.log Logs\app3.log", "--report handlers"],
                    ([r"Logs\app1.log", r"Logs\app2.log", r"Logs\app3.log"], "handlers")
            ),
            (
                    ["main.py", "--report unknown_report", r"Logs\app1.log"],
                    ([r"Logs\app1.log"], "unknown_report")
            ),
            (["main.py"], ([], None)),
        ]
    )
    def test_parse_args(self, argv, res, monkeypatch):
        monkeypatch.setattr("sys.argv", argv)
        assert parse_args() == res

    @pytest.mark.parametrize(
        "argv",
        [
            (
                    ["main.py", r"Logs\app1.log Logs\app2.log Logs\app3.log", "--report handlers"]
            ),
            (
                    ["main.py", "--report unknown_report", r"Logs\app1.log"],
            ),
            (["main.py"]),
        ]
    )
    def test_report_generation(self, argv, monkeypatch):
        monkeypatch.setattr("sys.argv", argv)
        report_generation()
