from flask import Flask

from config import host, port
from views import services

app = Flask(__name__)
app.register_blueprint(services.routes, url_prefix='/api/v1/services')

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
