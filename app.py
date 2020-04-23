# -- coding: utf-8 --
from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import pymysql

# init flask
app = Flask(__name__,
            template_folder="./dist",
            static_folder="./dist",
            static_url_path="")


# VUE ROUTER
@app.route('/')
def index():
    return render_template("index.html")


# init api
api = Api(app)

# init cors
CORS(app)

# init db
testdb = pymysql.connect(
    user="admin",
    password="1234",
    host="0.0.0.0",
    db="testdb",
    charset="utf8"
)
cursor = testdb.cursor(pymysql.cursors.DictCursor)


# REST API
class TaskAPI(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("task", type=str)
            args = parser.parse_args()

            sql = f"INSERT INTO task (task) VALUES ('{args['task']}');"
            cursor.execute(sql)
            testdb.commit()

            sql = "SELECT LAST_INSERT_ID();"
            cursor.execute(sql)
            response = cursor.fetchall()
            return jsonify(response[0])
        except Exception as error:
            return {"status": error}

    def get(self):
        try:
            cursor.execute("SELECT * FROM task;")
            response = cursor.fetchall()
            return jsonify(response)
        except Exception as error:
            return {"status": error}

    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("_id", type=int)
            parser.add_argument("done", type=int)
            args = parser.parse_args()

            sql = f"UPDATE task SET done={args['done']} WHERE _id={args['_id']}"
            cursor.execute(sql)
            testdb.commit()

            sql = f"SELECT * FROM task WHERE _id={args['_id']}"
            cursor.execute(sql)
            response = cursor.fetchall()
            return jsonify(response)
        except Exception as error:
            return {"status": error}

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("_id", type=int)
            args = parser.parse_args()

            sql = f"DELETE FROM task WHERE _id={args['_id']}"
            cursor.execute(sql)
            testdb.commit()

            return
        except Exception as error:
            return {"status": error}


# API ROUTER
api.add_resource(TaskAPI, "/task")
