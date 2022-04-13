# Copyright (c) 2022 Shutterfly. All rights reserved.

from sqlalchemy import text

from sfly.ppt.environment.cleaner_service import config
from sfly.ppt.environment.cleaner_service.formatter import print_table
from sfly.ppt.environment.cleaner_service.repository.engine import get_connection, in_transaction


def clean_environment():
    print("Running Clean...")
    dry_run = config.dry_run
    env = config.env_to_clean

    for tenant in config.tenants:
        tenant_conn = get_connection(tenant, config.tenants_config[tenant].get('database'))
        source_conn = get_connection(tenant, config.source_database)
        camunda_conn = get_connection(tenant, config.tenants_config[tenant].get('camunda_database'))

        with in_transaction(tenant_conn, source_conn):
            __clean_tenant(tenant, env, dry_run, tenant_conn=tenant_conn)
            __clean_orders(tenant, env, dry_run, source_conn=source_conn)
            __clean_camunda(tenant, env, dry_run, camunda_conn=camunda_conn)


def __clean_tenant(tenant, env: str = "qa", dry_run: bool = False, **kwargs):
    conn = kwargs.get('tenant_conn')
    __clean(
        env,
        tenant,
        [
            f'tenant_product_service_{env}.component_inst_virtual_state',
            f'tenant_product_service_{env}.component_inst_asset',
            f'tenant_product_service_{env}.component_priority_id',
            f'tenant_product_service_{env}.hold_meta_data',
            f'tenant_product_service_{env}.product_inst_priority_id',
            f'tenant_product_service_{env}.source_order_item_product',
            f'tenant_product_service_{env}.product_relator',
            f'tenant_product_service_{env}.component_inst',
            f'tenant_product_service_{env}.qc_hold',
            f'tenant_product_service_{env}.product_inst',
            f'tenant_order_lambda_service_{env}.manufacturing_order'
        ]
        , conn, dry_run)


def __clean_orders(tenant: str, env: str = "qa", dry_run: bool = False, **kwargs):
    source_conn = kwargs.get('source_conn')

    __clean(
        env,
        tenant,
        [
            f'source_domain_services_{env}.source_sub_order_item_asset',
            f'source_domain_services_{env}.source_sub_order_item',
            f'source_domain_services_{env}.source_sub_order',
            f'source_domain_services_{env}.order_change',
            f'source_domain_services_{env}.source_order'

        ], source_conn, dry_run)


def __clean_camunda(tenant, env: str, dry_run: bool = False, **kwargs):
    camunda_conn = kwargs.get('camunda_conn')

    __clean(
        env,
        tenant,
        [
            "act_hi_attachment",
            "act_hi_batch",
            "act_hi_caseactinst",
            "act_hi_caseinst,"
            "act_hi_comment",
            "act_hi_dec_in",
            "act_hi_dec_out",
            "act_hi_decinst",
            "act_hi_detail",
            "act_hi_ext_task_log",
            "act_hi_identitylink",
            "act_hi_incident",
            "act_hi_job_log",
            "act_hi_op_log",
            "act_hi_procinst",
            "act_hi_taskinst",
            "act_hi_varinst",
            "act_id_info",
            "act_re_case_def",
            "act_re_decision_def",
            "act_re_decision_req_def",
            "act_ru_batch",
            "act_ru_case_execution",
            "act_ru_case_sentry_part",
            "act_ru_event_subscr",
            "act_ru_variable",
            "act_ru_incident",
            "act_ru_ext_task",
            "act_ru_execution",
            "act_ru_filter",
            "act_ru_identitylink",
            "act_ru_job",
            "act_ru_jobdef",
            "act_ru_meter_log",
            "act_ru_task"

        ], camunda_conn, dry_run)


def __clean(evn, tenant, tables: [], conn, dry_run: bool):
    should_clean = False
    tables_info = []

    for table in tables:
        row = conn.execute(text(f'SELECT COUNT(*) AS total FROM {table}'))
        total = next(row).total
        tables_info.append({
            "table": table,
            "records": str(total)
        })
        if not should_clean:
            should_clean = total > 0

    print_table(tenant, evn, conn.engine.url.database, tables_info)

    if not dry_run and should_clean:
        conn.execute(text(f'TRUNCATE TABLE {",".join(tables)}'))
        print(f"Records deleted")

    print("\n")
