from flask import Flask
from flask_script import Manager
from App.searchView import search_blue

app = Flask(__name__)
#注册蓝图
app.register_blueprint(blueprint=search_blue)

manager = Manager(app=app)

if __name__ == '__main__':
    app.run()