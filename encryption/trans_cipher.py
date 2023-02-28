#!/usr/bin/env python3


import base64
import pprint
import hashlib
import binascii
import urllib.parse as parse

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from py3rijndael import RijndaelCbc, ZeroPadding

init_vactor = ''
block_size = 32
encry_key = ''

class transfer_cipher:

    def __init__(self):
        self.IV          = '{init_vactor}'
        self.BLOCK_SIZE  = block_size

    # 구 암호화 복호화
    def old_decrypt(self, value):
        key = self.hash_key(encry_key)
        iv  = self.hash_IV(self.IV)

        cipher = base64.b64decode(parse.unquote_plus(base64.b64decode(value).decode('UTF-8')))

        rijndael_cbc = RijndaelCbc(
            key        = key,
            iv         = iv,
            padding    = ZeroPadding(self.BLOCK_SIZE),
            block_size = self.BLOCK_SIZE
        )

        decrypt_text = rijndael_cbc.decrypt(cipher)
        plain_text = self.fromPkcs7(decrypt_text)
        return plain_text.decode()

    # 이전 신규 암호화
    def web_decrypt(self, value):
        encrypt_text, iv = value.split(':')
        iv               = iv.encode('UTF-8')
        key              = hashlib.sha256((encry_key).encode('UTF-8')).hexdigest()[:32].encode('UTF-8')

        decrypt_text = base64.b64decode(base64.b64decode(encrypt_text))
        cipher       = AES.new(key, AES.MODE_CBC, iv)
        decrypt      = cipher.decrypt(decrypt_text)

        return unpad(decrypt, AES.block_size).decode('UTF-8')

    # 구 암호문 uppadding
    def fromPkcs7(self, value):
        padlen = int(value[-1])
        pad    = value[len(value)-padlen:]
        if padlen > len(value):
            return ''

        for i in range(padlen):
            if pad[i] != padlen:
                return ''

        return value[:len(value)-padlen]

    # hash key 생성
    def hash_key(self, encry_key):
        hash_key = ''

        hash_key = hashlib.md5((
                hashlib.md5(encry_key.encode()).hexdigest()).encode()
        ).hexdigest()

        return hash_key

    # hash init vector 생성
    def hash_IV(self, IV):
        hex_IV = binascii.unhexlify(IV)
        md5_str = hashlib.md5(hashlib.md5(hex_IV).hexdigest().encode())

        hex2bin_str = binascii.unhexlify(md5_str.hexdigest())
        IV_hax = hashlib.md5(hashlib.md5(hex2bin_str).hexdigest().encode())

        return IV_hax.hexdigest()

    # 신규 암호화
    def new_encrypt(self, value):
        key = self.hash_key(encry_key).encode('UTF-8')
        iv  = self.hash_IV(self.IV)[:16].encode('UTF-8')

        cipher   = AES.new(key, AES.MODE_CBC, iv)
        pad_text = pad(value.encode('UTF-8'), AES.block_size)
        cipher_text = base64.b64encode(cipher.encrypt(pad_text)).decode('UTF-8')
        result      = base64.b64encode(parse.quote_plus(cipher_text).encode('UTF-8'))

        return str(iv.decode('UTF-8')) + "." + str(result.decode('UTF-8'))

    # 신규 복호화
    def new_decrypt(self, value):
        key = self.hash_key(key).encode('UTF-8')
        iv  = self.hash_IV(self.IV)[:16].encode('UTF-8')

        iv_check, cipher_text = value.split('.')

        if iv != iv_check.encode('UTF-8'):
            return ''

        cipher_text = parse.unquote_plus(base64.b64decode(cipher_text).decode('UTF-8'))
        cipher      = AES.new(key, AES.MODE_CBC, iv)
        decrypt     = unpad(cipher.decrypt(base64.b64decode(cipher_text)), AES.block_size)

        return decrypt.decode('UTF-8')

    # 암호문 교환
    # (구) 암호문 -> 평문 -> (신) 암호문
    # 평문 -> (신) 암호문
    # (신) 암호문 pass
    def trans_data(self, value):
        if value is None:
            return ''
        iv = self.hash_IV(self.IV)[:16]
        result = ''
        if value.startswith(iv):
            return value
        else:
            if not self.isBase64(value):
                if ':' in value:
                    web_dec = self.web_decrypt(value)
                    result  = self.new_encrypt(web_dec)
                else:
                    result = self.new_encrypt(value)
            else:
                old_dec = self.old_decrypt(value)
                result  = self.new_encrypt(old_dec)

        return result

    # (구) 암호화인지 평문인지 체크
    def isBase64(self, value):
        try :
            if isinstance(value, str):
                value_bytes = bytes(value, 'ascii')
            elif isinstance(value, bytes):
                value_bytes = value
            else :
                raise ValueError('Argument must be string or bytes')
            return base64.b64encode(base64.b64decode(value_bytes)) == value_bytes
        except Exception:
            return False

if __name__ == '__main__':
    transfer = transfer_cipher('')
    ctext = '';
    ptext = ''
    test = transfer.trans_data(ctext)
    pprint.pprint(test)

