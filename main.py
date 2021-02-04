from flask import Flask, render_template, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Todo
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True 
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:20220620@localhost:3306/todolistapi' 
db.init_app(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/todos/user/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def todos(username):
    if request.method == 'GET':
        todo = Todo.query.filter_by(username=username).first()
        if not todo:
            return jsonify({"msg": "user not found!"})

        return jsonify(todo.serialize()), 200

    if request.method == 'POST':

        # Solicitando el BODY
        body = request.get_json()
        # Validacion del BODY
        if type(body) != list:
            return jsonify({"msg": "not found!"}), 400
        # Task de placeholder
        body.append({"label": "sample task", "done": "false"})
        # Instancia del MODELO
        todo = Todo()
        # Establecer Username
        todo.username = username
        # Convertir en STRING
        todo.tasks = json.dumps(body)
        todo.save()

        return jsonify({"result": "ok"}), 201

    if request.method == 'PUT':

        body = request.get_json()
        # Definiendo body y localizando el user
        todo = Todo.query.filter_by(username=username).first()

        #VALIDANDO
        if todo:
            todo.tasks = json.dumps(body) #GUARDARLO EN BODY
            todo.update()
            return jsonify({"msg": "list with " + str(len(body)) + " todos was succesfully saved!"}), 200
        else:
            return jsonify({"msg": "user not found!"}), 400


    if request.method == 'DELETE':
        todos = Todo.query.filter_by(username=username).first()

        if not todos:
            return jsonify({"msg": "user not found!"}), 400

        todos.delete()

        return jsonify({"msg": "deleted!"}), 200

if __name__ == '__main__':
    manager.run()