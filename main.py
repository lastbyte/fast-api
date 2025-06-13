
from app.server import create_app
from app.common.configuration import config
import uvicorn

app = create_app()

def main():
    uvicorn.run(app=app, host="0.0.0.0", port=config.APP_PORT)


if __name__ == "__main__":
    main()
