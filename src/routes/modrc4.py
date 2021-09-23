import json
import logging
from flask import Blueprint, request, jsonify, send_file
from services import modrc4_decrypt, modrc4_encrypt

modrc4 = Blueprint('modrc4', __name__, url_prefix='/modrc4')


@modrc4.route('/encrypt/<string:input_type>', methods=['POST'])
def encrypt(input_type: str):
    try:
        if input_type == 'file':
            pass

        elif input_type == 'text':
            # Getting input parameters
            json_body = json.loads(request.data)
            _input = json_body['input']
            key = json_body['key']

            # Processing input
            byte_input = bytes(_input, 'utf-8')
            byte_key = bytes(key, 'utf-8')

            res = modrc4_encrypt(byte_input, byte_key)

            return jsonify(res), 200

        else:
            raise Exception(f'Invalid input type: {input_type}')

    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400


@modrc4.route('/decrypt/<string:input_type>', methods=['POST'])
def decrypt(input_type: str):
    try:
        if input_type == 'file':
            pass

        elif input_type == 'text':
            # Getting input parameters
            json_body = json.loads(request.data)
            _input = json_body['input']
            key = json_body['key']

            # Processing input
            byte_key = bytes(key, 'utf-8')

            res = modrc4_decrypt(_input, byte_key)

            return res.decode('utf-8'), 200

        else:
            raise Exception(f'Invalid input type: {input_type}')

    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400
