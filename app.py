from agent.agent import Agent
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

agent = Agent()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["message"]
    response = agent.respond(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)


