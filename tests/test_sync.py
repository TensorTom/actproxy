import requests
import toml
import actproxy
from actproxy import Data, Null, FlatList

store = toml.load('secrets.toml')
ACT_KEYS = [
	store['act']['api_keys'][0],
	store['act']['api_keys'][1]
]
INITIALIZED = False
ECHO_URL = 'https://ipecho.net/plain'


def test_init():
	global INITIALIZED
	api_resp = actproxy.init(ACT_KEYS)
	assert api_resp not in (None, Null)
	assert isinstance(api_resp, FlatList)
	assert len(api_resp) > 0
	assert isinstance(api_resp[0], Data)
	assert 'host' in api_resp[0] and 'port' in api_resp[0] \
	       and 'username' in api_resp[0] and 'password' in api_resp[0]
	INITIALIZED = True


def test_rotate():
	global INITIALIZED
	assert INITIALIZED is True
	proxy = actproxy.rotate()
	assert isinstance(proxy, Data)
	resp = requests.get(ECHO_URL, proxies=proxy)
	assert resp.status_code == 200
	remote_ip = resp.text
	assert remote_ip in proxy.https


def test_random_proxy():
	global INITIALIZED
	assert INITIALIZED is True
	proxy = actproxy.random_proxy()
	assert isinstance(proxy, Data)
	resp = requests.get(ECHO_URL, proxies=proxy)
	assert resp.status_code == 200
	remote_ip = resp.text
	assert remote_ip in proxy.https
