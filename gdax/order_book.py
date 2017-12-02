import gdax, requests, json
import base64, hashlib, hmac, time
from requests.auth import AuthBase

api_key = 'f2b4fc5543ee85bb080ee6f531fcc8d8'
api_secret = 'F0dgsc8gszR0MCoLyL0wXiFxIL6VP4lo5qdbPArgfpO6od94bIExEdie1CeDuo7AKIodzTCc873iR8GiYltFWw=='
passphrase = 'Snyf2933'
api_base = 'https://api-public.sandbox.gdax.com'


class GDAXRequestAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
def buy_market(product_id, size):
    auth = GDAXRequestAuth(api_key, api_secret, passphrase)
    order_data = {
        'type': 'market',
        'side': 'buy',
        'product_id': product_id,
        'size': size
    }
    response = requests.post(api_base + '/orders', data=json.dumps(order_data), auth=auth)
    if response.status_code is not 200:
        raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
    return response.json()

def order_status(order_id):
    order_url = api_base + '/orders/' + order_id
    response = requests.get(order_url, auth=auth)
    if response.status_code is not 200:
        raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
    return response.json()

auth = GDAXRequestAuth(api_key, api_secret, passphrase)
order_data = {
    'type': 'market',
    'side': 'buy',
    'product_id': 'BTC-USD',
    'size': '0.01'
}

# order_url = api_base + '/orders'
# response = requests.post(order_url, data=json.dumps(order_data), auth=auth)
# print(response.json())

publicClient = gdax.PublicClient();

order_book = publicClient.get_product_order_book(product_id='BTC-USD')
order_book.start()
print(order_book.get_asks(12000))
print(order_book.get_current_ticker());
time.sleep(10)
order_book.close()