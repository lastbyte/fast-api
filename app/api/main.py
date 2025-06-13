import importlib
import os
from fastapi import FastAPI
from app.common.logger import Logger

from app.common.constants import API_PREFIX


API_DIRECTORY = "app/api"

logger = Logger(__name__);

def add_api_routes(app: FastAPI):
    add_api_routes_from_directory(app, API_PREFIX)
    return app

def add_api_routes_from_directory(app: FastAPI, prefix: str):
    api_dir_path = os.path.abspath(API_DIRECTORY)

    for folder, _, files in os.walk(api_dir_path):

        relative_path = os.path.relpath(folder, api_dir_path)
        api_prefix =  relative_path.replace(os.sep, "/")

        if not api_prefix.startswith("/"):
            api_prefix = prefix + "/" + api_prefix

        for file in files:
            if file.endswith(".py") and file != "__init__.py" and file != "main.py":
                module_name = os.path.splitext(file)[0]

                module_path= f'app.api{(folder.split(f"app/api")[-1]).replace(os.sep, ".")}.{module_name}'
                module = importlib.import_module(module_path)

                if hasattr(module, "router"):
                    app.include_router(module.router, prefix=api_prefix)
