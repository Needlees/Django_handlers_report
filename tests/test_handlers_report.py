import pytest
from contextlib import nullcontext as does_not_raise

from src.handlers_report import log_processing, handlers_report


class TestHandlersReport:
    @pytest.mark.parametrize(
        "log, res, expectation",
        [
            (r'Logs\app1.log',
             {'/api/v1/reviews/': {'DEBUG': 0, 'INFO': 5, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
              '/admin/dashboard/': {'DEBUG': 0, 'INFO': 6, 'WARNING': 0, 'ERROR': 2, 'CRITICAL': 0},
              '/api/v1/users/': {'DEBUG': 0, 'INFO': 4, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
              '/api/v1/cart/': {'DEBUG': 0, 'INFO': 3, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
              '/api/v1/products/': {'DEBUG': 0, 'INFO': 3, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
              '/api/v1/support/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 3, 'CRITICAL': 0},
              '/api/v1/auth/login/': {'DEBUG': 0, 'INFO': 4, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0},
              '/admin/login/': {'DEBUG': 0, 'INFO': 5, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0},
              '/api/v1/checkout/': {'DEBUG': 0, 'INFO': 6, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0},
              '/api/v1/payments/': {'DEBUG': 0, 'INFO': 7, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0},
              '/api/v1/orders/': {'DEBUG': 0, 'INFO': 2, 'WARNING': 0, 'ERROR': 2, 'CRITICAL': 0},
              '/api/v1/shipping/': {'DEBUG': 0, 'INFO': 2, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0}}, does_not_raise()
             ),
            (r'Logs\NotFound.log', {}, pytest.raises(FileNotFoundError))
        ]
    )
    def test_log_processing(self, log, res, expectation):
        with expectation:
            assert log_processing(log) == res

    @pytest.mark.parametrize(
        "file_logs, res",
        [
            ([r'Logs\app1.log', r'Logs\app2.log'],
             ([['HANDLER', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], ['/admin/dashboard/', 0, 10, 0, 3, 0],
               ['/admin/login/', 0, 8, 0, 2, 0], ['/api/v1/auth/login/', 0, 7, 0, 1, 0],
               ['/api/v1/cart/', 0, 4, 0, 0, 0], ['/api/v1/checkout/', 0, 11, 0, 2, 0],
               ['/api/v1/orders/', 0, 6, 0, 3, 0], ['/api/v1/payments/', 0, 10, 0, 2, 0],
               ['/api/v1/products/', 0, 8, 0, 3, 0], ['/api/v1/reviews/', 0, 13, 0, 1, 0],
               ['/api/v1/shipping/', 0, 5, 0, 2, 0], ['/api/v1/support/', 0, 9, 0, 3, 0],
               ['/api/v1/users/', 0, 7, 0, 2, 0]], 'requests')
             )
        ]
    )
    def test_handlers_report(self, file_logs, res):
        assert handlers_report(file_logs) == res
