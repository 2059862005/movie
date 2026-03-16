import hashlib
import urllib.parse
from datetime import datetime
from django.conf import settings

class Alipay:
    def __init__(self):
        self.app_id = getattr(settings, 'ALIPAY_APP_ID', '')
        self.private_key = getattr(settings, 'ALIPAY_PRIVATE_KEY', '')
        self.alipay_public_key = getattr(settings, 'ALIPAY_PUBLIC_KEY', '')
        self.gateway = 'https://openapi.alipay.com/gateway.do'
        self.notify_url = getattr(settings, 'ALIPAY_NOTIFY_URL', '')
        self.return_url = getattr(settings, 'ALIPAY_RETURN_URL', '')

    def sign(self, params):
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        unsigned_string = '&'.join(f'{k}={v}' for k, v in sorted_params if v)
        sign = hashlib.sha256(unsigned_string.encode('utf-8') + self.private_key.encode('utf-8')).hexdigest()
        return sign

    def build_url(self, out_trade_no, subject, total_amount):
        params = {
            'app_id': self.app_id,
            'method': 'alipay.trade.page.pay',
            'format': 'JSON',
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0',
            'notify_url': self.notify_url,
            'return_url': self.return_url,
            'out_trade_no': out_trade_no,
            'total_amount': str(total_amount),
            'subject': subject,
            'product_code': 'FAST_INSTANT_TRADE_PAY',
        }
        params['sign'] = self.sign(params)
        return f"{self.gateway}?{urllib.parse.urlencode(params)}"

    def verify(self, params):
        sign = params.pop('sign', '')
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        unsigned_string = '&'.join(f'{k}={v}' for k, v in sorted_params if v)
        expected_sign = hashlib.sha256(unsigned_string.encode('utf-8') + self.alipay_public_key.encode('utf-8')).hexdigest()
        return sign == expected_sign
