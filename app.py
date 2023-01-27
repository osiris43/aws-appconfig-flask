from random import randint
from flask import Flask
import os, requests

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello from index"


@app.route("/rolldice")
def roll_dice():
    flag_enabled = get_single_flag("development", "can-roll-dice")
    if not flag_enabled:
        return "You are not old enough to roll dice sir or madam"

    response = "You are allowed to play and rolled a {0}".format(do_roll())
    return response


def do_roll():
    return randint(1, 6)


def get_single_flag(environment, flag):
    if environment == "local":
        return False

    url = "{0}{1}".format("http://localhost:2772", build_environment_url(environment))
    r = requests.get(url)
    flags = r.json()
    app.logger.debug("%s flags", flags)
    return flags[flag]["enabled"]


def build_environment_url(environment):
    return (
        "/applications/your-application/environments/"
        "{0}"
        "/configurations/your-config-name"
    ).format(environment)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
