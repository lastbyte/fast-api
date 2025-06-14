from fastapi import FastAPI
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
    configure_openapi(app)
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


def configure_openapi(app: FastAPI):
    @app.get("/openapi.json", include_in_schema=False)
    async def get_openapi_json():
        return get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
    return app
