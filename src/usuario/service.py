from flask import jsonify,request
from utils import database,funciones, mailing

import hashlib
import hmac
import datetime
import socket
import json

def securityServiceTokenValid(token):
    try:
        return {'status': True, 'data': 'rulman'}  
    except Exception as e:
        return {'status': False,'data':str(e)}

def usuarioServicioCrearUsuario():
    try:
        bdapp = database.Connection()
        body = request.json
        email = body['email']
        query = """SELECT email FROM tausuario WHERE email='%s'""" % email
        response = bdapp.queryfetchone(query)
        if response['status'] :
            if response['data']:
                return jsonify({'msg': 'Email Exist'}), 409
            else:
                serverMail = mailing.Conecction()
                code = funciones.randomString(40)
                redirect = 'http://localhost/kinecitas/#/validar/' + code 
                html_content='<strong>Validar <a target="_blank" href="'+ redirect+'">VALIDAR CORREO</a></strong>'
                
                responseMail=serverMail.sendMail('rulman26@gmail.com','Validar email',html_content)
                print(responseMail)
                query = """INSERT INTO tausuario 
                            VALUES(default,'%s','kinecitas','%s',1,'A','')
                            """%(email , code)
                response = bdapp.queryInsert(query)
                if response['status'] :
                    return jsonify(response['data'])
                else:
                    return jsonify({ 'MySql Error' : response['data'] }), 500  
        else:
            return jsonify({ 'MySql Error' : response['data'] }), 500  
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()


def usuarioServicioValidarUsuario():
    try:
        bdapp = database.Connection()
        body = request.json
        code = body['code']
        password = body['password']
        query = """SELECT id FROM tausuario WHERE codigo='%s'""" % code
        response = bdapp.queryfetchone(query)
        if response['status'] :
            if response['data']:
                idUsuario=int(response['data']['id'])
                hash=funciones.hash_password(password)
                print(hash)
                query = """UPDATE tausuario SET password='%s' WHERE id=%i"""%(hash , idUsuario)
                response = bdapp.queryUpdate(query)
                if response['status'] :
                    return jsonify(response['data']), 201
                else:
                    return jsonify({ 'MySql Error' : response['data'] }), 500 
            else:
                return jsonify({'msg': 'Codigo No valido'}), 204
        else:
            return jsonify({ 'MySql Error' : response['data'] }), 500  
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()

def usuarioServicioLoginUsuario():
    try:
        bdapp = database.Connection()
        body = request.json
        email = body['email']
        password = body['password']
        query = """SELECT password FROM tausuario WHERE email='%s'""" % email
        response = bdapp.queryfetchone(query)
        if response['status'] :
            if response['data']:
                password_store = response['data']['password']
                valido = funciones.verify_password(password_store,password)
                if  valido:
                    query="""SELECT a.id,a.email,a.perfil_id,b.nombre redirect
                            FROM tausuario a
                            JOIN gnusuarioperfil b on b.id=a.perfil_id
                            where email='%s'
                            """ % email
                    response = bdapp.queryfetchone(query)
                    if response['status']:
                        token ="asdasdasd"
                        query="""UPDATE tausuario SET token='%s' WHERE id=%i""" % (token ,response['data']['id'])
                        update = bdapp.queryUpdate(query)
                        if update['status']:
                            response['data']['token'] = token
                            print(response['data'])
                            return jsonify(response['data'])
                        else:
                            return jsonify({ 'MySql Error' : update['data'] }), 500   
                    else:
                        return jsonify({ 'MySql Error' : response['data'] }), 500   
                else:
                    return jsonify({'msg': 'Credenciales Incorrectas'}), 409 
            else:
                return jsonify({'msg': 'Email no Existe'}), 204
        else:
            return jsonify({ 'MySql Error' : response['data'] }), 500  
    except Exception as e:
        print("Log => " + str(e))
        return jsonify({'msg': str(e)}), 500
    finally:
        bdapp.close()
        