#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:45:18 2020

@author: mag
"""

# This example uses Python 2.7 and the python-request library.

from flask import Flask
from pymongo import MongoClient
from flask import jsonify, request, redirect, url_for
from flask_cors import CORS
from conexion_api import get_data
from conexion_mongo import conectar_db_cripto, conectar_db_cripto2
import json

from hasheo import hasheo_base, hashear

app = Flask(__name__)
CORS(app)

# Funcion para iniciar bd
def iniciar_bases():
    db = conectar_db_cripto()
    db.cryp.drop()  #vaciamos la db
    data = get_data()
    # print(data)
    db.cryp.insert_many(data)  # inserto datos en db
    data = db.cryp.find({}, {"_id": 0})  # obtener datos de la db
    hash_data = hasheo_base(data)  #hashear la data para insertar en la db2
    # print(hash_data)
    db2 = conectar_db_cripto2()
    db2.cryp.drop()
    db2.cryp.insert_many(hash_data)  #Insertamos la data hasheada en la db2
    print('ok')


# inicializamos cuando arranca la app
iniciar_bases()


# validacion para buscar x  id
def validacionDos(item, db2):
    aux = False
    # hasheo la data y la busco en la bdd hasheada para ver si coincide
    data1 = hashear(item)
    data2 = db2.cryp.find_one({"cmc_rank": item["cmc_rank"]}, {
                              "_id": 0})  # buscar en base al ranking
    if (data1 == data2["hash"]):
        aux = True
    else:
        aux = False

    return aux


# Obtener una criptomoneda por id
@app.route('/obtenerSegunId', methods=['POST'])
def obtenerSegunId():
    try:
        if request.method == 'POST':
            id = request.json['id']
            print(id)
            db = conectar_db_cripto()
            db2 = conectar_db_cripto2()
            aux = db.cryp.find_one({"id": str(id)}, {"_id": 0})
            # print(res)
            if (aux != None) and (validacionDos(aux, db2) == False):
                raise Exception('error info')
            return jsonify(aux)
    except (Exception) as err:
        return str(err), 500


# Borrar criptomoneda
@app.route('/borrarCrypto', methods=['POST'])
def borrarCrypto():
    try:
        if request.method == 'POST':
            #id = request.json['id']
            rank = request.json['rank']
            db = conectar_db_cripto()
            db2 = conectar_db_cripto2()
            db.cryp.delete_one({"cmc_rank": str(rank)})
            db2.cryp.delete_one({"cmc_rank": str(rank)})
            # db.cryp.delete_one({"id":str(id)})
            # db2.cryp.delete_one({"id":str(id)})

            return "deleted"
    except (Exception) as err:
        return str(err), 500


# validacion para cuando quiero obtener todas las cryptomonedas, #top 5 y top20
def validacion(db1_cryp, db2):
    aux = False
    for i in db1_cryp:
        data1 = hashear(i)
        data2 = db2.cryp.find_one({"cmc_rank": i["cmc_rank"]}, {"_id": 0})
        # verifico si el resultado de la bdd 1 es igual a la hasheada
        if (data1 == data2["hash"]):
            aux = True
        else:
            aux = False

    return aux



# Listar criptomonedas
@app.route('/listarTodasCrypto', methods=['GET'])
def listarTodasCrypto():
    if request.method == 'GET':
        db = conectar_db_cripto()
        db2 = conectar_db_cripto2()
        aux = []
        for x in db.cryp.find({}, {"_id": 0}):
            aux.append(x)
        if (validacion(aux, db2) == False) or (db.cryp.count() != db2.cryp.count()):
            print('informacion erronea')
        return jsonify(aux)



# Listar top5
@app.route('/top5', methods=['GET'])
def top5():
    if request.method == 'GET':
        db = conectar_db_cripto()
        db2 = conectar_db_cripto2()
        aux = []
        for x in db.cryp.find({"$where": "parseInt(this.cmc_rank) <=5"}, {"_id": 0}):
            aux.append(x)
            # print(aux)
        if (validacion(aux, db2) == False) or (db.cryp.count() != db2.cryp.count()):
            print('informacion erronea')
        return jsonify(aux)



# Listar top20
@app.route('/top20', methods=['GET'])
def top20():
    if request.method == 'GET':
        db = conectar_db_cripto()
        db2 = conectar_db_cripto2()
        aux = []

        for x in db.cryp.find({"$where": "parseInt(this.cmc_rank) <=20"}, {"_id": 0}):
            aux.append(x)
            # print(aux)
        if (validacion(aux, db2) == False) or (db.cryp.count() != db2.cryp.count()):
            print('informacion erronea')
        return jsonify(aux)


if __name__ == '__main__':
    app.run(host='backend', port='5000', debug=True)
