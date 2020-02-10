from flask import Blueprint,jsonify,request
from .service import *
from functools import wraps
kinecita = Blueprint('kinecita' , __name__)

def token_requiered(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is Missing'}), 403
        try:
            headers = token.split()
            if (len(headers) != 2):
                return jsonify({'message': 'Token is Missing'}), 403
            data = securityServiceTokenValid(headers[1])
            if(not data['status']):
                return jsonify({'message': 'Token is Invalid'}), 403
        except:
            return jsonify({'message': 'Token is Invalid'}), 403
        return f(*args, **kwargs)
    return decorated


@kinecita.route('/formdatos' , methods=['GET'] )
@token_requiered
def formDatosKinecita():
    return kinecitaServiceFormDatos()


