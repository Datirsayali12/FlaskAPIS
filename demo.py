from flask import Flask, jsonify, request, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


def check_db_connection():

        conn= mysql.connector.connect(
            host='localhost',      # Replace with your MySQL server host
            user='root',  # Replace with your MySQL username
            password='root',  # Replace with your MySQL password
            database='demo'   # Replace with your database name
        )
        return conn


@app.route('/get-data/',methods=["GET"])
def get_data():
    conn=check_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute("select * from users")
    data=cur.fetchall()
    print(data)
    cur.close()
    conn.close()

    return jsonify(data)

@app.route('/get/<int:id>/',methods=["GET","PUT","DELETE"])
def get_single_data(id):
    conn = check_db_connection()
    cur = conn.cursor(dictionary=True)
    if request.method=="GET":
        cur.execute("select name from users where id = %s",(id,))
        data=cur.fetchone()
        cur.close()
        conn.close()

        return jsonify({"message":"the data is sucessfully get","dtaa":data}),200

    if request.method=="PUT":
        data=request.json
        name=data.get("name")
        cur.execute("update  users set name= %s where id=%s",(name,id))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message":"data is sucessfully updated"}),200

    if request.method=="DELETE":
        cur.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message":"data deleted sucessfully"}),200



@app.route("/save-data/",methods=["POST"])
def save_data():
    conn=check_db_connection()
    cur=conn.cursor()
    data=request.json
    try:
        name=data.get("name")
        id=data.get("id")
    except Exception as e:
        return jsonify({"message":"invalid data"}),400

    cur.execute("insert into users(id,name) values(%s,%s)",(id,name))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message":"data inserted sucessfully"}),200



@app.route('/app')
def app_data():
    conn=check_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute("select * from users")
    data=cur.fetchall()
    cur.close()
    conn.close()

    message="hello to all"

    return render_template('index.html',message=data)


if __name__ == '__main__':
    app.run(debug=True)
