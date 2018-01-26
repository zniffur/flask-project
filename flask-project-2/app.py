from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    lst = [1,2,4,3,5,7,9,13,45,44,68,124]
    # return "hello"
    return render_template("index.html", nums=lst)


if __name__ == "__main__":
    # app.debug = True
    app.run(host="0.0.0.0", port=8000)
