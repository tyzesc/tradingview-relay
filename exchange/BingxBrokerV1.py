# coding: utf-8
import os
import urllib.request
import json
import base64
import hmac
import time

APIURL = os.getenv("BINGX_APIURL")
APIKEY = os.getenv("BINGX_APIKEY")
SECRETKEY = os.getenv("BINGX_SECRETKEY")


def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(
        SECRETKEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256"
    ).digest()


def post(url, body):
    req = urllib.request.Request(
        url, data=body.encode("utf-8"), headers={"User-Agent": "Mozilla/5.0"}
    )
    return urllib.request.urlopen(req).read()


class BingxBrokerV1:
    def __init__(self) -> None:
        pass

    def call(self, path="/", method="GET", params={}, payload={}):
        paramsMap = {"apiKey": APIKEY, "timestamp": int(time.time() * 1000)}
        # concat params
        paramsMap.update(params)
        sortedKeys = sorted(paramsMap)
        paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
        paramsStr += "&sign=" + urllib.parse.quote(
            base64.b64encode(genSignature(path, method, paramsMap))
        )
        if method == "POST":
            return json.loads(post(APIURL + path, paramsStr))
        else:
            print("Not support method: %s" % method)

    def get_balance(self):
        paramsMap = {"currency": "USDT"}
        return self.call("/api/v1/user/getBalance", "POST", paramsMap)

    def get_positions(self, symbol):
        paramsMap = {}
        return self.call("/api/v1/user/getPositions", "POST", paramsMap)

    def place_order(
        self,
        symbol,
        side,
        price,
        volume,
        tradeType,
        action,
        takerProfitPrice,
        stopLossPrice,
    ):
        paramsMap = {
            "symbol": symbol,
            "side": side,
            "entrustPrice": price,
            "entrustVolume": volume,
            "tradeType": tradeType,
            "action": action,
            "takerProfitPrice": takerProfitPrice,
            "stopLossPrice": stopLossPrice,
        }

        if takerProfitPrice == None:
            paramsMap.pop("takerProfitPrice")
        if stopLossPrice == None:
            paramsMap.pop("stopLossPrice")
        return self.call("/api/v1/user/trade", "POST", paramsMap)

    def order_buy_limit(
        self, symbol, price, volume, takerProfitPrice=None, stopLossPrice=None
    ):
        return self.place_order(
            symbol,
            "Bid",
            price,
            volume,
            "Limit",
            "Open",
            takerProfitPrice,
            stopLossPrice,
        )

    def order_sell_limit(
        self, symbol, price, volume, takerProfitPrice=None, stopLossPrice=None
    ):
        return self.place_order(
            symbol,
            "Ask",
            price,
            volume,
            "Limit",
            "Open",
            takerProfitPrice,
            stopLossPrice,
        )

    def order_buy_market(
        self, symbol, volume, takerProfitPrice=None, stopLossPrice=None
    ):
        return self.place_order(
            symbol,
            "Bid",
            0,
            volume,
            "Market",
            "Open",
            takerProfitPrice,
            stopLossPrice,
        )

    def order_sell_market(
        self, symbol, volume, takerProfitPrice=None, stopLossPrice=None
    ):
        return self.place_order(
            symbol,
            "Ask",
            0,
            volume,
            "Market",
            "Open",
            takerProfitPrice,
            stopLossPrice,
        )