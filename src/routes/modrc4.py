from flask import Blueprint

modrc4 = Blueprint('modrc4', __name__, url_prefix='/modrc4')


@modrc4.route('/encrypt', methods=['POST'])
def encrypt():
    pass


@modrc4.route('/decrypt', methods=['POST'])
def decrypt():
    pass
