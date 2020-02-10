from flask import jsonify,request
from utils import database,funciones, mailing

import hashlib
import hmac
import datetime
import socket
import json

def securityServiceTokenValid(token):
    try:
        bdapp = database.Connection()
        query = "select id,email from tausuario where token='%s'"
        response = bdapp.queryfetchone(query % (token))
        if(response['data']):
            return {'status': True, 'data': response['data']}
        else:
            return {'status': False, 'data': 'Token Invalid'}
    except Exception as e:
        return {'status': False,'data':str(e)}
    finally:
        bdapp.close()      

def kinecitaServiceFormDatos():
    try:
        bdapp = database.Connection()
        query = "SELECT id,nombre FROM tapais WHERE estado='A'"
        response = bdapp.queryfetchall(query)
        result = {}
        if response['status'] :
            result['paises'] = response['data']
            query = "select id,nombre from taetnia where estado='A'"
            response = bdapp.queryfetchall(query)
            if response['status'] :
                result['etnias'] = response['data']
                query = "select id,nombre from taservicio where estado='A'"
                response = bdapp.queryfetchall(query)
                if response['status'] :
                    result['servicios'] = response['data']
                    query = "select id,nombre from taservicioespecial where estado='A'"
                    response = bdapp.queryfetchall(query)
                    if response['status'] :
                        result['especiales'] = response['data']
                        return jsonify(result)
                    else:
                        return jsonify({ 'MySql Error taservicioespecial' : response['data'] }), 500 
                else:
                    return jsonify({ 'MySql Error taservicio' : response['data'] }), 500 
            else:
                return jsonify({ 'MySql Error taetnia' : response['data'] }), 500  
        else:
            return jsonify({ 'MySql Error tapais' : response['data'] }), 500  
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()

        