from os import environ
from wsgiref.simple_server import WSGIServer

from main import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    app.secret_key = "SuPeR_SeCReT_KeY"
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True, threaded=True)
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
