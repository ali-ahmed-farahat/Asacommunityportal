from agent.agent import Agent
import os
from flask import Flask, render_template, request, jsonify
from agent.search_vdb import search
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["message"]
    # Create a new agent instance for each request
    agent = Agent()
    response = agent.respond(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )


