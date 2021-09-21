from flask import Blueprint

stegano = Blueprint('stegano', __name__, url_prefix='/stegano')


@stegano.route('/hide', methods=['POST'])
def hide(file_type):
    pass


@stegano.route('/show', methods=['POST'])
def show(file_type):
    pass
