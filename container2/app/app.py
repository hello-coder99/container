from flask import Flask
import mysql.connector
import os 
app=Flask(__name__)
@app.route("/",methods=["GET"])
def home():
    conn=mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_DATABASE"]
        )
    cursor=conn.cursor()
    cursor.execute("SELECT VERSION();")
    db_version=cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return f"connected to the maria db of version {db_version}"
if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)

    


