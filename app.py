from flask import Flask, Response, render_template
from time import sleep
from loguru import logger
import datetime

logger.add("app/static/job.log", format="{time} - {message}")

APP = Flask(__name__, static_folder="app/static/", template_folder="app/static/")
@APP.route("/", methods=["GET"])
def root():
    """index page"""
    return render_template("index.html")



# adjusted flask_logger
def flask_logger():
    """creates logging information"""
    with open("app/static/job.log") as log_info:
        for i in range(25):
            logger.info(f"iteration #{i}")
            data = log_info.read()
            yield data.encode()
            sleep(1)
        # Create empty job.log, old logging will be deleted
        open("app/static/job.log", 'w').close()



@APP.route("/log_stream", methods=["GET"])
def log_stream():
    """returns logging information"""
    return Response(flask_logger(), mimetype="text/plain", content_type="text/event-stream")


if __name__ == "__main__":
    APP.run(port=5000, threaded=True)