# Copyright (c) 2022 Shutterfly. All rights reserved.
from sfly.ppt.environment.cleaner_service.repository import database  # pragma: no cover

if __name__ == '__main__':  # pragma: no cover
    try:
        database.clean_environment()
    except Exception as e:
        print(e)
