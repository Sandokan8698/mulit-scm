# Copyright (c) 2022 Shutterfly. All rights reserved.
from logging import getLogger

from sqlalchemy import text

from sfly.ppt.environment.cleaner_service import config
from sfly.ppt.environment.cleaner_service.repository.engine import get_connection, in_transaction

log = getLogger("environment-data-service.database")


def clean_environment():
    dry_run = config.dry_run
    env = config.env_to_clean

    for tenant in config.tenants:
        product_conn = get_connection(tenant, config.tenants_config[tenant].get('database'))
        source_conn = get_connection(tenant, config.source_database)
        with in_transaction(product_conn, source_conn):
            __clean_products(env, dry_run, product_conn=product_conn)
            __clean_orders(env, dry_run, product_conn=product_conn, source_conn=source_conn)


def __clean_products(env: str = "qa", dry_run: bool = False, **kwargs):
    conn = kwargs.get('product_conn')
    __clean(f'tenant_product_service_{env}.component_inst_virtual_state', conn, dry_run)
    __clean(f'tenant_product_service_{env}.component_inst_asset', conn, dry_run)
    __clean(f'tenant_product_service_{env}.component_priority_id', conn, dry_run)
    __clean(f'tenant_product_service_{env}.hold_meta_data', conn, dry_run)
    __clean(f'tenant_product_service_{env}.product_inst_priority_id', conn, dry_run)
    __clean(f'tenant_product_service_{env}.source_order_item_product', conn, dry_run)
    __clean(f'tenant_product_service_{env}.product_relator', conn, dry_run)
    __clean(f'tenant_product_service_{env}.component_inst', conn, dry_run)
    __clean(f'tenant_product_service_{env}.qc_hold', conn, dry_run)
    __clean(f'tenant_product_service_{env}.product_inst', conn, dry_run)


def __clean_orders(env: str = "qa", dry_run: bool = False, **kwargs):
    source_conn = kwargs.get('source_conn')
    product_conn = kwargs.get('product_conn')

    __clean(f'tenant_order_lambda_service_{env}.manufacturing_order', product_conn, dry_run)
    __clean(f'source_domain_services_{env}.source_sub_order_item_asset', source_conn, dry_run)
    __clean(f'source_domain_services_{env}.source_sub_order_item', source_conn, dry_run)
    __clean(f'source_domain_services_{env}.source_sub_order', source_conn, dry_run)
    __clean(f'source_domain_services_{env}.order_change', source_conn, dry_run)
    __clean(f'source_domain_services_{env}.source_order', source_conn, dry_run)


def __clean(table: str, conn, dry_run: bool):
    row = conn.execute(text(f'SELECT COUNT(*) AS total FROM {table}'))
    total = next(row).total
    print(f"Total records to delete from {table}: {total}")

    if total == 0:
        print("No records to delete")
        return

    if not dry_run:
        print("Deleting records")
        conn.execute(text(f'DELETE FROM {table} where true'))
        print("Records deleted")
