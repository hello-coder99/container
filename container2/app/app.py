from flask import Flask
import mysql.connector
import os 
app=Flask(__name__)
@app.route("/",method=["GET"])
def home():
    conn=mysql.connector(
        host=os.getenv("DB_HOST")
        username=os.getenv("DB_USERNAME")
        password=os.getenv("DB_PASSWORD")
        database=os.getenv("DB_DATABASE")
        )
    cursor=conn.cursor()
    cursor.execute("SELECT VERSION();")
    db_version=cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return f"connected to the maria db of version {db_version}"
if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)

    


