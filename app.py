from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    reply = "Page loaded successfully"

    if request.method == "POST":
        user_input = request.form["message"]
        reply = "You said: " + user_input

    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(debug=False)

