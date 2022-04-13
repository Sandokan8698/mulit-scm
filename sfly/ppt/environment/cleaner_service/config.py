# Copyright (c) 2022 Shutterfly. All rights reserved.
from os import getenv

region = getenv("AWS_REGION", "us-east-1")
tenants = getenv("TENANTS", 'formtill,msp').split(",")
dry_run = True if getenv("DRY_RUN", 'true') == 'true' else False
env_to_clean = getenv("ENV_TO_CLEAN", "qa")

source_database = getenv("SOURCE_DATABASE", "source")
username = getenv("DB_CREDS_USR", "admin")
password = getenv("DB_CREDS_PSW", "admin")

tenants_config = {
    "ftm": {
        "server": getenv("FTM_SERVER", "localhost"),
        "port": getenv("FTM_PORT", "5432"),
        "database": getenv("FTM_DATABASE", "fortmill"),
        "camunda_database": getenv("FTM__CAMUNDA_DATABASE", "camunda-ftm")
    },
    "msp": {
        "server": getenv("MSP_SERVER", "localhost"),
        "port": getenv("MSP_PORT", "5432"),
        "database": getenv("MSP_DATABASE", "root"),
        "camunda_database": getenv("MSP_CAMUNDA_DATABASE", "camunda-msp")
    },
    "tpe": {
        "server": getenv("TPE_SERVER", "localhost"),
        "port": getenv("TPE_PORT", "5432"),
        "database": getenv("TPE_DATABASE", "root"),
        "camunda_database": getenv("TPE_CAMUNDA_DATABASE", "camunda-tpe")
    },
    "dfw": {
        "server": getenv("DFW_SERVER", "localhost"),
        "port": getenv("DFW_PORT", "5432"),
        "database": getenv("DFW_DATABASE", "root"),
        "camunda_database": getenv("DFW_CAMUNDA_DATABASE", "camunda-dfw")
    }
}
