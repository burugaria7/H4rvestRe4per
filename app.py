from flask import Flask, render_template

APP = Flask(__name__, static_folder="/app/static/", template_folder="app/static/")
@APP.route("/", methods=["GET"])
def root():
    """index page"""
    return render_template("index.html")


if __name__ == "__main__":
    APP.run(port=8080, threaded=True)