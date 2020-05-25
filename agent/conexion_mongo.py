#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:48:53 2020

@author: mag
"""

# This example uses Python 2.7 and the python-request library.


from pymongo import MongoClient


def conectar_db_cripto():
    client = MongoClient(host='db_cripto', port=27017)
    data_base = client.get_database('crypto_coins')
    print('ok')
    return data_base


def conectar_db_cripto2():
    client = MongoClient(host='db_cripto2', port=27017)
    data_base = client.get_database('crypto_coins')
    print('ok')
    return data_base
