from typing import List


def print_table(tenant: str, env, schema: str, schema_tables: List[dict]):
    print(f"Environment: {env} Tenant: {tenant} Schema: {schema}")
    print("{:<80} {:<10}".format('Tables', 'Records'))
    for schema_table in schema_tables:
        print("{:<80} {:<10}".format(schema_table["table"], schema_table["records"]))
