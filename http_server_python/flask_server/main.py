from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def foo():
    return "Hello World!\n"

@app.route("/", methods=["POST"])
def bar():
    req = request.json
    return f"Hello {req['field']}"

if __name__ == "__main__":
    print("Server starts on [0.0.0.0:50051]")
    app.run(host="0.0.0.0", port=50001)
