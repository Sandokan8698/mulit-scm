# Copyright (c) 2022 Shutterfly. All rights reserved.
import logging
from os import getenv

logging.basicConfig(level=logging.INFO)

tenants = getenv("TENANTS", 'ftm').split(",")
dry_run = True if getenv("DRY_RUN", 'true') == 'true' else False
env_to_clean = getenv("ENV_TO_CLEAN", "qa")

source_database = getenv("SOURCE_DATABASE", "source")
username = getenv("DB_CREDS_USR", "root")
password = getenv("DB_CREDS_PSW", "root")

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
