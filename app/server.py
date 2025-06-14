import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.api.main import add_api_routes
from app.common.constants import APP_NAME, APP_DESCRIPTION
from app.common.logger import Logger
from app.connectors.db.postgres import create_db_and_tables
from app.middlewares.rate_limiter import RateLimiterMiddleware
from fastapi.openapi.utils import get_openapi


logger = Logger(__name__);

def create_app():
    try:
        app = FastAPI(title=APP_NAME, description=APP_DESCRIPTION)
        return configure_app(app)
    except Exception as e:
        logger.error(f"Error creating app: {e}")
        raise e


def configure_app(app: FastAPI):
    configure_database(app)
    configure_routers(app)
    configure_middlewares(app)
    configure_swagger_json(app)
    return app


def configure_swagger_json(app: FastAPI):
    @app.on_event("startup")
    def get_swagger_json():
        # save the swagger.json to the static folder
        with open("swagger.json", "w") as f:
            f.write(json.dumps(get_openapi(title=APP_NAME, description=APP_DESCRIPTION, version="1.0.0", routes=app.routes), indent=10))
    return app

def configure_database(app : FastAPI):
    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()
    return app
    
def configure_routers(app: FastAPI):
    try:
        add_api_routes(app)
    except Exception as e:
        logger.error(f"Error creating app: {e}")
        raise e
    return app


def configure_middlewares(app: FastAPI):

    # add the rate limiter middleware
    app.add_middleware(RateLimiterMiddleware, max_requests=20, time_window=60)
    return app

