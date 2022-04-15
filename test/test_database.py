import collections
from unittest.mock import patch, Mock

from sfly.ppt.environment.cleaner_service.repository.database import __clean_tenant, __clean_orders, __clean_camunda, \
    clean_environment, __clean


def get_result(query):
    total = 1 if "no_empty" in query.text else 0
    Result = collections.namedtuple('Result', 'total')
    yield Result(total=total)


def test_clean_should_not_execute_truncate_if_dry_run():
    conn = Mock()
    execute = Mock(side_effect=get_result)
    conn.execute = execute

    __clean("qa", "ftm", ["empty"], conn, True)
    assert execute.call_count == 1


def test_clean_should_not_execute_truncate_table_is_empty():
    conn = Mock()
    execute = Mock(side_effect=get_result)
    conn.execute = execute

    __clean("qa", "ftm", ["empty"], conn, False)
    assert execute.call_count == 1


def test_clean_should_execute_if_not_dry_run_and_not_empty_table():
    conn = Mock()
    execute = Mock(side_effect=get_result)
    conn.execute = execute

    __clean("qa", "ftm", ["no_empty"], conn, False)
    assert execute.call_count == 2
    assert execute.call_args[0][0].text == 'TRUNCATE TABLE no_empty'


@patch("sfly.ppt.environment.cleaner_service.repository.database.__clean")
def test_clean_tenant(clean):
    __clean_tenant("ftm", "qa", True, tenant_conn=None)
    assert clean.call_count == 1
    assert clean.call_args_list == [(('qa', 'ftm', ['tenant_product_service_qa.component_inst_virtual_state',
                                                    'tenant_product_service_qa.component_inst_asset',
                                                    'tenant_product_service_qa.component_priority_id',
                                                    'tenant_product_service_qa.hold_meta_data',
                                                    'tenant_product_service_qa.product_inst_priority_id',
                                                    'tenant_product_service_qa.source_order_item_product',
                                                    'tenant_product_service_qa.product_relator',
                                                    'tenant_product_service_qa.component_inst',
                                                    'tenant_product_service_qa.qc_hold',
                                                    'tenant_product_service_qa.product_inst',
                                                    'tenant_order_lambda_service_qa.manufacturing_order'], None,
                                      True),)]


@patch("sfly.ppt.environment.cleaner_service.repository.database.__clean")
def test_clean_orders(clean):
    __clean_orders("ftm", "qa", True, tenant_conn=None)
    assert clean.call_count == 1
    assert clean.call_args_list == [(('qa', 'ftm', ['source_domain_services_qa.source_sub_order_item_asset',
                                                    'source_domain_services_qa.source_sub_order_item',
                                                    'source_domain_services_qa.source_sub_order',
                                                    'source_domain_services_qa.order_change',
                                                    'source_domain_services_qa.source_order'], None, True),)]


@patch("sfly.ppt.environment.cleaner_service.repository.database.__clean")
def test_clean_camunda(clean):
    __clean_camunda("ftm", "qa", True, tenant_conn=None)
    assert clean.call_count == 1
    assert clean.call_args_list == [(('qa', 'ftm', ['act_hi_attachment', 'act_hi_batch', 'act_hi_caseactinst',
                                                    'act_hi_caseinst,act_hi_comment', 'act_hi_dec_in',
                                                    'act_hi_dec_out', 'act_hi_decinst', 'act_hi_detail',
                                                    'act_hi_ext_task_log', 'act_hi_identitylink', 'act_hi_incident',
                                                    'act_hi_job_log', 'act_hi_op_log', 'act_hi_procinst',
                                                    'act_hi_taskinst', 'act_hi_varinst', 'act_id_info',
                                                    'act_re_case_def', 'act_re_decision_def',
                                                    'act_re_decision_req_def', 'act_ru_batch',
                                                    'act_ru_case_execution', 'act_ru_case_sentry_part',
                                                    'act_ru_event_subscr', 'act_ru_variable', 'act_ru_incident',
                                                    'act_ru_ext_task', 'act_ru_execution', 'act_ru_filter',
                                                    'act_ru_identitylink', 'act_ru_job', 'act_ru_jobdef',
                                                    'act_ru_meter_log', 'act_ru_task'], None, True),)]


@patch("sfly.ppt.environment.cleaner_service.repository.database.__clean_camunda")
@patch("sfly.ppt.environment.cleaner_service.repository.database.__clean_orders")
@patch("sfly.ppt.environment.cleaner_service.repository.database.__clean_tenant")
@patch("sfly.ppt.environment.cleaner_service.repository.database.in_transaction")
@patch("sfly.ppt.environment.cleaner_service.repository.database.get_connection")
def test_clean_environment(get_connection, in_transaction, clean_tenant, clean_orders, clean_camunda):
    conn = [
        {"tenant_conn": "tenant_conn"},
        {"source_conn": "source_conn"},
        {"camunda_conn": "camunda_conn"}
    ]
    get_connection.side_effect = conn
    clean_environment()
    assert get_connection.call_count == 3
    assert in_transaction.call_count == 1
    assert clean_tenant.call_count == 1
    assert clean_orders.call_count == 1
    assert clean_camunda.call_count == 1

    assert conn[0] == clean_tenant.call_args_list[0][1].get('tenant_conn')
    assert conn[1] == clean_orders.call_args_list[0][1].get('source_conn')
    assert conn[2] == clean_camunda.call_args_list[0][1].get('camunda_conn')
