from flask import Flask

core = Flask(__name__)

@core.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    core.run(debug=True, host='0.0.0.0', port=5000)