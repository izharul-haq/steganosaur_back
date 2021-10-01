from flask import Blueprint, request, jsonify, send_file, send_from_directory
from services import image_stegano

stegano = Blueprint('stegano', __name__, url_prefix='/stegano')

@stegano.route('/hide/image/', methods=['POST'])
def hide_image(file_type):
    try:   
        buffer = request.files['input']
        cover = request.files['mask']
        key = request.form.get('key') # key, already have default value
        mode = request.form.get('mode') # true kalo seq, false, random.

        # Preprocessing input
        # Encode the message in a serie of 8-bit values
        mask_data, width, height = read_cover_image(buffer)
        mask_data = flatten_image(mask_data)
        input_data = cover.read()
        input_data = ''.join(["{:08b}".format(ord(x)) for x in input_data]) # read every byte 
        input_data = [int(x) for x in input_data] # read every bit
        
        filetype = filename.split('.')[-1]

        # Processing input
        res = encrypt_steg_image(mask_data, input_data, mode, key) #get pixel data
        res = construct_image(res, width,height) # construct pixel data
    
        # construct image
        new_img = Image.fromarray(data)
    
        with open(f'bin/steg-encrypt.{filetype}', 'wb') as f:
            f.write(new_img)
        f.close()

        return send_file(f'..bin/steg-encrypt.{filetype}')
    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400

@stegano.route('/show/image', methods=['POST'])
def show_image(file_type):
    try:   
        buffer = request.files['input']
        key = request.form.get('key') # key, already have default value
        mode = request.form.get('mode') # true kalo seq, false, random.

        # Preprocessing input
        # Encode the message in a serie of 8-bit values
        mask_data, width, height = read_cover_image(buffer)
        mask_data = flatten_image(mask_data)        
        filetype = filename.split('.')[-1]

        # Processing input
        res = decrypt_steg_image(mask_data, key) # get bits data
        byte = []
        for i in range(len(res)):
            s = ''.join(str(res[i]))
            if i % 7 == 0:
                byte.append("08b".join(s))
                s = ''
    
        with open(f'bin/steg-decrypt.{filetype}', 'wb') as f:
            f.write(byte)
        f.close()

        return send_file(f'..bin/steg-encrypt.{filetype}')
    except Exception as e:
        logging.exception(str(e))
        return jsonify({'code': 400, 'message': str(e)}), 400
