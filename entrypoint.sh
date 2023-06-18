# check environment variables
if [ -z "$PASSPHRASE" ]; then
  echo "environment variable: PASSPHRASE is not set"
  exit 1
fi

if [ -z "$BINGX_APIURL" ]; then
  echo "environment variable: BINGX_APIURL is not set"
  exit 1
fi

if [ -z "$BINGX_APIKEY" ]; then
  echo "environment variable: BINGX_APIKEY is not set"
  exit 1
fi

if [ -z "$BINGX_SECRETKEY" ]; then
  echo "environment variable: BINGX_SECRETKEY is not set"
  exit 1
fi

# start tradingview-relay
python3 -u tradingview-relay.py