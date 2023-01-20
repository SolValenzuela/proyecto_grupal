from flask import Flask

app = Flask("Google Login App")
app = Flask(__name__)

app.secret_key = "shhhhhh"