from flask import Flask

app = Flask(__name__)

# define route for the root URL ("/")
@app.route("/")
def index():
    # function handles requests to the root URL
    return {"message": "Hello World"}
