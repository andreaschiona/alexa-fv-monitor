"""
WiseSolar Plus API Client
=========================
Client per le API cloud WiseSolar Plus (autenticazione AES-ECB).
Utilizzato da Lambda (Alexa skill) e fv_cron.py (Hermes).
"""
import os, json, hashlib, time, base64, ssl, urllib.parse, urllib.request, urllib.error

# AES keys from WiseSolar platform
PWD_KEY = b'clxslychxyl11988'
VERCODE_KEY = b'%vSBtRMV4F8mr#dYofsG3lJOBv5vw*fZ'
BASE_URL = 'https://www.wisesolarplus.com/necp'

# Lazy import pyaes
_aes = None

def _get_aes():
    global _aes
    if _aes is None:
        try:
            import pyaes
            class AESHandle:
                MODE_ECB = None
                @classmethod
                def new(cls, key, mode):
                    return cls(key)
                def __init__(self, key):
                    self.key = key
                def encrypt(self, data):
                    aes = pyaes.AESModeOfOperationECB(self.key)
                    return b''.join(aes.encrypt(data[i:i+16]) for i in range(0, len(data), 16))
            _aes = AESHandle()
        except ImportError:
            raise RuntimeError('pyaes not installed. pip install pyaes')
    return _aes

def _aes_encrypt(plaintext):
    aes = _get_aes()
    data = plaintext.encode()
    pad_len = 16 - (len(data) % 16)
    return base64.b64encode(aes.encrypt(data + bytes([pad_len] * pad_len))).decode()

def _sign(params):
    sorted_str = ','.join(f"{k}={params[k]}" for k in sorted(params.keys()))
    md5 = hashlib.md5(sorted_str.encode()).hexdigest().lower()
    timestamp = str(int(time.time() * 1000))
    digest = f'{md5},{timestamp}'
    if digest.startswith(','):
        digest = digest[1:]
    aes = _get_aes()
    data = digest.encode()
    pad_len = 16 - (len(data) % 16)
    return base64.b64encode(aes.encrypt(data + bytes([pad_len] * pad_len))).decode()

def api_call(path, params, token=''):
    url = BASE_URL + path
    body = urllib.parse.urlencode(params).encode()
    sign = _sign(params)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'sign': sign,
        'version': '6.0.0',
        'channelType': '2',
        'os': 'android',
        'clientType': 'Android',
        'locale': 'en',
        'authorization': token,
        'token': token,
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 14)',
    }
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {'code': '-1', 'msg': str(e)}

def login(username, password):
    encrypted_pwd = _aes_encrypt(password)
    resp = api_call('/login/appLogin2', {'username': username, 'password': encrypted_pwd})
    if str(resp.get('code')) != '0':
        raise RuntimeError(f"Login failed: {resp.get('message', 'unknown error')}")
    return resp['data']['token']

def get_realtime(station_id, token):
    resp = api_call('/app/Plant/getEmsPlantDetailInfo', {'stationId': str(station_id)}, token)
    if str(resp.get('code')) != '0':
        return None
    data = resp['data']
    rt = data.get('plantRealTimeData', {})
    si = data.get('stationInfo', {})
    weather = (data.get('weathers') or [{}])[0]
    return {
        'pv_power': int(float((rt.get('pvPower') or 0)) * 1000),
        'grid_power': int(float((rt.get('gridPower') or 0)) * 1000),
        'load_power': int(float((rt.get('loadPower') or 0)) * 1000),
        'battery_power': int(float((rt.get('batteryPower') or 0)) * 1000),
        'status': int(si.get('stationStatus', 3)),
        'has_battery': si.get('esCapacity') is not None,
        'weather': weather.get('weatherDesc', '') + ' ' + weather.get('temperature', ''),
    }

def get_stats(station_id, token):
    resp = api_call('/app/Plant/getPlantDetailConciseInfo', {'stationId': str(station_id)}, token)
    if str(resp.get('code')) != '0':
        return None
    kd = resp['data'].get('keyData', {})
    return {
        'day_energy': float(kd.get('dayElec', 0) or 0),
        'total_energy': float((kd.get('totalElec', 0) or 0)) * 1000,
        'day_consumption': float(kd.get('dayConsum', 0) or 0),
    }

def get_revenue(customer_id, token):
    resp = api_call('/app/customer/statistics', {'customerId': str(customer_id)}, token)
    if str(resp.get('code')) != '0':
        return 0.0
    return float(resp.get('data', {}).get('dayIncome', 0) or 0)

def get_all_data():
    """Get all FV data. Reads config from environment variables."""
    username = os.environ.get('FV_USER', '')
    password = os.environ.get('FV_PASS', '')
    station_id = os.environ.get('FV_STATION_ID', '3680')
    customer_id = os.environ.get('FV_CUSTOMER_ID', '3176')

    if not username or not password:
        raise RuntimeError('FV_USER and FV_PASS environment variables required')

    token = login(username, password)
    realtime = get_realtime(station_id, token)
    stats = get_stats(station_id, token)
    revenue = get_revenue(customer_id, token)

    if not realtime or not stats:
        raise RuntimeError('Failed to fetch FV data from WiseSolar API')

    status_map = {1: 'Normal', 2: 'Offline', 3: 'Abnormal'}
    st = realtime['status']
    status_text = status_map.get(st, f'Unknown ({st})')
    if st == 3 and not realtime['has_battery']:
        status_text = 'Normal'

    return {
        'pv_power': realtime['pv_power'],
        'grid_power': realtime['grid_power'],
        'load_power': realtime['load_power'],
        'battery_power': realtime['battery_power'],
        'status': status_text,
        'weather': realtime['weather'],
        'day_energy': stats['day_energy'],
        'total_energy': stats['total_energy'],
        'day_consumption': stats['day_consumption'],
        'revenue': revenue,
    }
