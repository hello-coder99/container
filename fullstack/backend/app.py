from flask import Flask, jsonify, request, session, redirect, url_for, render_template
import redis
import os
import mysql.connector

app = Flask(__name__)

# ✅ Redis client (fix host)
redis_client = redis.Redis(
    host='redis',   # 'redis' hose as (matches docker-compose service name)
    port=6379,
    decode_responses=True
)
def connection():
    conn=mysql.connector.connect(
            host=os.environ["MYSQL_HOST"],
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"]
        )
    return conn
def init_db():
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            uid INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(50) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cursor.close()
# Call this once when Flask starts
# ✅ MySQL connection (reads from .env via Docker Compose)
@app.route('/api/export',methods=['POST'])
def export_file():
    data=request.get_json()
    email=data.get('email')
    password=data.get('password')
    if not (email and password):
        return jsonify({"error":"invalid credentials"}), 400
    try:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT name,email,password FROM users WHERE email=%s",(email,))
        text=cursor.fetchone()
        if password==text[2]:
            with open("userdata.txt",'w') as file:
                file.write(str(text))
            return jsonify({"message":"successfully written"}), 201
    except Exception:
        return jsonify({"error":"unable to fulfil requests"}), 500 
    finally:
        cursor.close()
        conn.close()

@app.route('/api/register',methods=['POST'])
def register():
    data=request.json
    name=data.get("name")
    email=data.get("email")
    password=data.get("password")
    if not (name and email and password):
        return jsonify({"error occured":"missing fields"}), 400
    try:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",(name,email,password))
        conn.commit()
        return jsonify({"success":"successfully user cred registered"}), 201
    except Exception as e:
        return jsonify({"error":"unable to register"}), 500
    finally:
        cursor.close()
        conn.close()
@app.route('/api/login',methods=['POST'])
def login():
    data=request.json
    email=data.get("email")
    password=data.get("password")
    if not (email and password):
        return jsonify({"error":"missing credentials"})
    try:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("SELECT name,email,password FROM users WHERE email=%s",(email,))
        cred=cursor.fetchone()
        if not cred:
            return jsonify({"error":"invalid user or password"}), 401
        if cred[2]==password:
            return jsonify({
                    "message":"Login successfull jack",
                    "user":{
                        "name":cred[0],
                        "email":cred[1],
                        "password":cred[2]
                        }
                    })
        
    except Exception as e:
        return jsonify({"error":"cannot login due to some error"}), 401
    finally:
        cursor.close()
        conn.close()
@app.route('/api', methods=["GET"])
def hello():
    redis_client.set("message", "Hello to my server! It uses MySQL, Redis, and Flask.")
    conn=connection()
    init_db()
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    return jsonify({
        "message": redis_client.get("message"),
        "database_time": result[0].isoformat()  # ✅ Optional format
    })
@app.route('/api/message',methods=["GET"])
def message():
    return {"message_from_host":"echo echo this is tesing message"}
@app.route("/api/submit", methods=["POST"])
def submit_message():
    data = request.get_json()
    name = data.get("name")
    message = data.get("message")
    conn=connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message))
    conn.commit()
    return jsonify({"message": "Message received and stored!"})
@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        conn=connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id,name,message,created_at FROM messages ORDER BY id DESC")
        data=cursor.fetchall()
        messages=[{"id":row[0],"name":row[1],"message":row[2],"datetime":row[3]} for row in data]
        cursor.close()
        conn.close()

        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/api/messages/<int:id>',methods=['DELETE'])
def delete_message(id):
    try:
        conn=connection()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM messages WHERE id=%s",(id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success":True,"message":f"message of id={id} deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

