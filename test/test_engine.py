from unittest.mock import Mock

from sfly.ppt.environment.cleaner_service.repository.engine import in_transaction


def test_in_transaction_should_rollback_if_exception():
    connection = Mock()
    transaction = Mock()
    connection.begin = Mock(side_effect=transaction)

    with in_transaction(connection):
        raise Exception
    assert "rollback" in transaction.mock_calls[1][0]


def test_in_transaction_should_commit():
    connection = Mock()
    transaction = Mock()
    connection.begin = Mock(side_effect=transaction)

    with in_transaction(connection):
        pass
    assert "commit" in transaction.mock_calls[1][0]
