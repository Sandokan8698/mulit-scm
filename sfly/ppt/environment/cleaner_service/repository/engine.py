# Copyright (c) 2022 Shutterfly. All rights reserved.
import contextlib
from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from sfly.ppt.environment.cleaner_service import config


def get_engine(tenant: str, database: str):  # pragma: no cover
    tenant_config = config.tenants_config.get(tenant)
    return create_engine(
        "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
            config.username,
            quote(config.password),
            tenant_config.get('server'),
            tenant_config.get('port'),
            database
        ),
        poolclass=NullPool
    )


def get_connection(tenant: str, database: str):
    return get_engine(tenant, database).connect()


@contextlib.contextmanager
def in_transaction(*connections):
    transactions = []
    try:
        for connection in connections:
            transactions.append(connection.begin())

        yield

        for transaction in transactions:
            transaction.commit()

    except Exception as e:
        for transaction in transactions:
            transaction.rollback()

        print(e)

    finally:

        # Close the connections
        for connection in connections:
            connection.close()
