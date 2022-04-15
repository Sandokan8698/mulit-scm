# Copyright (c) 2022 Shutterfly. All rights reserved.
import contextlib
from logging import getLogger
from urllib.parse import quote

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from sfly.ppt.environment.cleaner_service import config

log = getLogger("environment-cleaner-service.engine")


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


def get_connection(tenant: str, database: str):  # pragma: no cover
    log.debug(f"Initializing connection for tenant {tenant} db {database}")
    return get_engine(tenant, database).connect()


@contextlib.contextmanager
def in_transaction(*connections):
    transactions = []
    try:
        for connection in connections:
            log.debug(f"Initializing transaction for db {connection.engine.url.database}")
            transactions.append(connection.begin())

        yield

        for transaction in transactions:
            log.debug(f"Committing transaction for db {transaction.connection.engine.url.database}")
            transaction.commit()

    except Exception as e:
        for transaction in transactions:
            log.debug(f"Rolling back transaction for db {transaction.connection.engine.url.database}")
            transaction.rollback()
        log.error(e)

    finally:

        # Close the connections
        for connection in connections:
            log.debug(f"Closing connection for db {connection.engine.url.database}")
            connection.close()
