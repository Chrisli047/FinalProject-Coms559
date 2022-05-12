import watchtower
import logging

from flask import Flask

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
handler = watchtower.CloudWatchLogHandler()
app.logger.addHandler(handler)
logging.getLogger("werkzeug").addHandler(handler)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
