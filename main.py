import time

import flask
import playwright.sync_api

app = flask.Flask(__name__)
from utils import solver


@app.route("/")
def index():
    return flask.redirect("https://github.com/Euro-pol/turnaround-api")


@app.route("/solve", methods=["POST"])
def solve():
    json_data = flask.request.json
    sitekey = json_data["sitekey"]
    invisible = json_data["invisible"]
    url = json_data["url"]
    proxy = json_data.get('proxy')
    user_agent = json_data.get('user_agent')
    with playwright.sync_api.sync_playwright() as p:
        s = solver.Solver(p, proxy, headless=True, user_agent=user_agent)
        start_time = time.time()
        token = s.solve(url, sitekey, invisible)
        print(f"took {time.time() - start_time} seconds :: " + token[:10])
        s.terminate()
        return make_response(token)


def make_response(captcha_key):
    if captcha_key == "failed":
        return flask.jsonify({"status": "error", "token": None})
    return flask.jsonify({"status": "success", "token": captcha_key})


if __name__ == "__main__":
    app.run()
