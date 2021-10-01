import logging
from flask import Blueprint, request, send_file, jsonify
from services import encrypt_audio, decrypt_audio, modrc4_crypt
import wave

stegano_audio = Blueprint('stegano_audio', __name__, url_prefix='/stegano')


@stegano_audio.route('/hide/audio', methods=['POST'])
def hide():
    try:
        mask = request.files['mask']
        content = request.files['content']

        key = request.form.get('key')
        mode = request.form.get('mode')

        buffer_mask = mask.read()
        buffer_content = content.read()

        # print(buffer_mask)
        with open('bin/stegano/audio/bin_mask.wav', 'wb') as f:
            f.write(buffer_mask)
        f.close()

        buffer_mask = 'bin/stegano/audio/bin_mask.wav'

        if key is not None:
            buffer_content = modrc4_crypt(buffer_content,bytes(key, 'utf-8'))
        
        res = None
        if mode == 'seq':
            res = encrypt_audio(buffer_content, buffer_mask, seq=True, key="STEGA")
        elif mode == 'rand':
            res = encrypt_audio(buffer_content, buffer_mask, seq=False, key="STEGA")
        else:
            raise Exception(f'Invalid mode: {mode}')

        # print(res)
        
        with wave.open("bin/stegano/audio/output.wav", 'wb') as fd:
            fd.setparams(res[0])
            fd.writeframes(res[1])

        return send_file(f'../bin/stegano/audio/output.wav')
    
    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400

@stegano_audio.route('/show/audio', methods=['POST'])
def show():
    try:

        masked_file = request.files['maskedfile']
        key = request.form.get('key')
        buffer_mask = masked_file.read()

        with open('bin/stegano/audio/bin_masked_file.wav', 'wb') as f:
            f.write(buffer_mask)
        f.close()

        buffer_mask = 'bin/stegano/audio/bin_masked_file.wav'

        res = decrypt_audio(buffer_mask, key="STEGA")

        with open(f'bin/stegano/audio/decrypted-audio.txt', 'wb') as f:
            f.write(res)
        f.close()

        return send_file(f'../bin/stegano/audio/decrypted-audio.txt')

    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400
