from pymongo import MongoClient
from bson.objectid import ObjectId


def conectar_ao_banco(host, port, banco, collection):
    try:
        client = MongoClient(host, port)
        banco = client[banco]
        colecao = banco[collection]
    except Exception as e:
        return str(e)

    return colecao


def find(colecao,query):

    try:

        lista_documentos = list(colecao.find(query))

        if (len(lista_documentos) > 0):
            return lista_documentos
        else:
            return []

    except Exception as e:
        return str(e)


def find_one_and_update(colecao, query, update):

    try:

        registro = colecao.find_one_and_update(
                                                query,
                                                { '$set': update },
                                                return_document = ReturnDocument.AFTER
                                                )

        if (registro != None):
            return registro

    except Exception as e:
        return str(e)

    return False


def update_many(colecao, query, update):

    try:

        registro = colecao.update_many(
                                        query,
                                        { '$set': update }
                                        )

    except Exception as e:
        return str(e)

    return True