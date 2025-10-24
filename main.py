import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home_page.html")


@app.route("/inputs")
def inputs():
    with open("inputs.json", "r") as f:
        data = json.loads(f.read())
    return data

if __name__ == '__main__':
    app.run(debug=True)




'''
@app.route("/animals")
def hello_world():
    return ["dogs", "cats", "birds"]

if __name__ == '__main__':
    app.run(debug=True)
'''


