# Copyright (c) 2019 Shutterfly. All rights reserved.
from os import getenv

region = getenv("AWS_REGION", "us-east-1")
tenants = getenv("TENANTS", 'formtill,msp').split(",")
dry_run = eval(getenv("DRY_RUN", True))
env_to_clean = getenv("ENV_TO_CLEAN", "qa")

source_database = getenv("SOURCE_DATABASE", "source")
username = getenv("USERNAME", "root")
password = getenv("PASSWORD", "root")

tenants_config = {
    "fortmill": {
        "server": getenv("FORTMILL_SERVER", "localhost"),
        "port": getenv("FORTMILL_PORT", "5432"),
        "database": getenv("FORTMILL_DATABASE", "fortmill")
    },
    "msp": {
        "server": getenv("MSP_SERVER", "localhost"),
        "port": getenv("MSP_PORT", "5432"),
        "database": getenv("MSP_DATABASE", "root")
    },
    "tpe": {
        "server": getenv("TPE_SERVER", "localhost"),
        "port": getenv("TPE_PORT", "5432"),
        "database": getenv("TPE_DATABASE", "root")
    },
    "dfw": {
        "server": getenv("DFW_SERVER", "localhost"),
        "port": getenv("DFW_PORT", "5432"),
        "database": getenv("DFW_DATABASE", "root")
    }
}
