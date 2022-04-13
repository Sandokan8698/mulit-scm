from typing import List

from rich.console import Console
from rich.table import Table

console = Console()


def print_table(tenant: str, env, schema: str, tables_info: List[dict]):
    table = Table(show_header=True, header_style="bold magenta", width=80)
    table.add_column("Table", width=70)
    table.add_column("Records", width=10)

    console.print(f"Environment: {env} Tenant: {tenant} Schema: {schema}")
    for table_info in tables_info:
        table.add_row(
            table_info.get("table"),
            table_info.get("records"))

    console.print(table)
