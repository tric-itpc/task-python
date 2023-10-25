from uvicorn import run

from routes.home import app
from settings import env

if __name__ == "__main__":
    run(
        app,
        host=env.SERVER_HOST,
        port=int(env.SERVER_PORT),
        ssl_certfile=env.SERVER_SSL_CERTFILE,
        ssl_keyfile=env.SERVER_SSL_KEYFILE,
    )