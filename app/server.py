from fastapi import FastAPI
from app.api.main import add_api_routes
from app.common.constants import APP_NAME, APP_DESCRIPTION
from app.common.logger import Logger
from app.connectors.db.postgres import create_db_and_tables
from app.middlewares.rate_limiter import RateLimiterMiddleware


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
