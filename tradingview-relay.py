import os
from flask import Flask, request, json
from prometheus_flask_exporter import PrometheusMetrics
from exchange.BingxBrokerV1 import BingxBrokerV1

import threading

bingx = BingxBrokerV1()

passphrase = os.getenv("PASSPHRASE")
app = Flask(__name__)
metrics = PrometheusMetrics(app)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


balance_metric = metrics.info(
    "balance", "Balance of USDT", labels={"exchange": "BINGX"}
)
equity_metric = metrics.info("equity", "Equity of USDT", labels={"exchange": "BINGX"})


def update_balance():
    global bingx
    res = bingx.get_balance()
    if res["code"] == 0:
        balance_metric.set(res["data"]["account"]["balance"])
        equity_metric.set(res["data"]["account"]["equity"])
    else:
        print(res)


by_path_counter = metrics.counter(
    "by_path_counter",
    "Request count by request paths",
    labels={"path": lambda: request.path},
)


@app.route("/")
@by_path_counter
def hello():
    text = "TradingViewRelay @tyzesc"
    return f"<h1 style='text-align: center; vertical-align: middle;'>{text}</h1>"


@app.route("/webhook", methods=["POST"])
@by_path_counter
def handler():
    data = request.data
    j = json.loads(data.decode("utf-8"))
    if "key" not in j or j["key"] != passphrase:
        return "Access Denied"
    print("Received data from TradingView")
    print(j)
    return "OK"


if __name__ == "__main__":
    set_interval(update_balance, 5)
    app.run(host="0.0.0.0", port=18105)
