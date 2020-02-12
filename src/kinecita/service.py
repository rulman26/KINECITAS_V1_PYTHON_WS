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
                return jsonify(result)
            else:
                return jsonify({ 'MySql Error taetnia' : response['data'] }), 500  
        else:
            return jsonify({ 'MySql Error tapais' : response['data'] }), 500  
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()
        

def kinecitaServicioCrearKinecita():
    try:
        bdapp = database.Connection()
        body = request.json
        id = body['id']
        telefono = body['telefono']
        nombres = body['nombres']
        edad = body['edad']
        pais = body['pais']
        etnia = body['etnia']
        query = "INSERT INTO takinesiologa VALUES(DEFAULT,'%s','%s',%i,'NO',%i,%i,%i,'A')"%(telefono , nombres , int(edad) , int(etnia) , int(pais) , int(id))
        response = bdapp.queryInsert(query)
        if response['status'] :
            return jsonify(response)
        else:
            return jsonify({ 'MySql Error tapais' : response['data'] }), 500  
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()

def kinecitaServicioVerKinecita(id):
    try:
        bdapp = database.Connection()
        query = """SELECT a.id,a.telefono,a.nombre,a.edad,a.etnia_id,b.nombre etnia_nombre,a.pais_id,c.nombre pais_nombre
                FROM takinesiologa a
                JOIN taetnia b on b.id=a.etnia_id
                JOIN tapais c on c.id=a.pais_id
                WHERE a.usuario_id=%i"""% id
        response = bdapp.queryfetchone(query)
        result = {}
        if response['status'] :
            return jsonify(response['data'])
        else:
            return jsonify({ 'MySql Error tapais' : response['data'] }), 500  
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()
    
def kinecitaServicioModificarKinecita():
    try:
        bdapp = database.Connection()
        body = request.json
        id = body['id']
        telefono = body['telefono']
        nombres = body['nombres']
        edad = body['edad']
        pais = body['pais']
        etnia = body['etnia']
        query = """UPDATE takinesiologa 
                    SET telefono='%s',
                        nombre = '%s',
                        edad = %i,
                        etnia_id = %i,
                        pais_id = %i
                    WHERE usuario_id=%i    
                    """%(telefono , nombres , int(edad) , int(etnia) , int(pais) , int(id))
        response = bdapp.queryUpdate(query)
        if response['status'] :
            return jsonify(response['data'])
        else:
            return jsonify({ 'MySql Error takinesiologa' : response['data'] }), 500
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()