import json
import logging
from flask import Blueprint, request, jsonify, send_file, send_from_directory
from services import modrc4_crypt

modrc4 = Blueprint('modrc4', __name__, url_prefix='/modrc4')


@modrc4.route('/encrypt/<string:input_type>', methods=['POST'])
def encrypt(input_type: str):
    try:
        if input_type == 'file':
            buffer = request.files['input']
            key = request.form.get('key')

            # Preprocessing input
            filename = buffer.filename
            filetype = filename.split('.')[-1]
            byte_key = bytes(key, 'utf-8')

            # Processing input
            res = modrc4_crypt(buffer.read(), byte_key)

            with open(f'bin/modrc4/mod-RC4-encrypted.{filetype}', 'wb') as f:
                f.write(res)
            f.close()

            return send_file(f'../bin/modrc4/mod-RC4-encrypted.{filetype}')

        elif input_type == 'text':
            # Getting input parameters
            json_body = json.loads(request.data)
            _input = json_body['input']
            key = json_body['key']

            # Preprocessing input
            byte_input = bytes(_input, 'utf-8')
            byte_key = bytes(key, 'utf-8')

            # Processing input
            res = modrc4_crypt(byte_input, byte_key)

            return jsonify([byte for byte in res]), 200

        else:
            raise Exception(f'Invalid input type: {input_type}')

    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400


@modrc4.route('/decrypt/<string:input_type>', methods=['POST'])
def decrypt(input_type: str):
    try:
        if input_type == 'file':
            buffer = request.files['input']
            key = request.form.get('key')

            # Preprocessing input
            filename = buffer.filename
            filetype = filename.split('.')[-1]
            byte_key = bytes(key, 'utf-8')

            # Processing input
            res = modrc4_crypt(buffer.read(), byte_key)

            with open(f'bin/modrc4/mod-RC4-decrypted.{filetype}', 'wb') as f:
                f.write(res)
            f.close()

            return send_file(f'../bin/modrc4/mod-RC4-decrypted.{filetype}')

        elif input_type == 'text':
            # Getting input parameters
            json_body = json.loads(request.data)
            _input = json_body['input']
            key = json_body['key']

            # Preprocessing input
            byte_key = bytes(key, 'utf-8')

            # Processing input
            res = modrc4_crypt(_input, byte_key)

            return res.decode('utf-8'), 200

        else:
            raise Exception(f'Invalid input type: {input_type}')

    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400
