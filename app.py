from flask import Flask, render_template, request, jsonify

from ice_breaker import Cooking

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/response")
def response():
    return render_template("response.html")


@app.route("/process", methods=["POST"])
def process():
    ingredients = request.form["ingredients"]
    ethnicity = request.form["ethnicity"]

    resp = Cooking("gpt-4o").recipe_creator(ingredients, ethnicity)
    return jsonify(resp)


if __name__ == "__main__":
    app.run(debug=True)
