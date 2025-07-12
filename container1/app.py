from flask import Flask
import os 
app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY","default-key")
@app.route("/")
def function():
    return f"so this is the api key {app.secret_key}"
if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000)
