import random
import urllib3
import couchdb2
import pycouchdb
import cryptocode
import base64
from lorem import *
from time import sleep
import tempfile


urllib3.disable_warnings()
ntfile = tempfile.NamedTemporaryFile()


db_url = 'https://username:password@dev.website.com:6984'
PASSCODE0 = "Tiew1fee3eequoo0fohhiilieW!ie"
PASSCODE1 = "Ee!thohx1ucheegh3aedeez4eiHeh"


def connect_http_db():  # only works with http without throwing fit errors.
    try:
        couchserver = couchdb2.Server(db_url)
        servername = db_url.rsplit('@')
        # for dbname in couchserver:  # gets list of database currently present
        #    print(dbname)
        available_dbs = []
        for dbname in couchserver:
            available_dbs.append(dbname.__str__())
        dbcount = len(available_dbs)
        # print(f'{dbcount} databases on http://{servername[1]} server. \n{available_dbs}')
        print(f'Connected to: {servername[1]}\n')
        return couchserver, available_dbs
    except Exception as e:
        print(e)


def connect_https_couchdb():  # preferred connection way. works with https and http
    try:
        couchserver = pycouchdb.Server(db_url)  # uses pycouchdb
        print(f'\n>>> Connected to {couchserver.base_url} \n')
        return couchserver
    except Exception as e:
        print(e)

#  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv-DB Section


def get_all_dbs():  # Get all databases from connected couchserver.
    try:
        i = 0o1
        dblist = []
        couchserver = connect_https_couchdb()
        servername = couchserver.base_url
        # print(f'\tCouchDB Server {servername}')
        sleep(1)
        print(f'\tNo. \tDatabase Name(s)')
        print('\t------------------------')
        for db in couchserver:  # for each database on the connected couchserver.
            # print(f'\t{i}.)\t{db}')
            dbno = i
            full_name = {"database_number": dbno, "database_name": db}
            dblist.append(full_name)
            i += 1
        sleep(.25)
        for eachdb in dblist:
            print(f"\t{eachdb['database_number'], eachdb['database_name']}")
        print(f"\t{len(dblist)}, total databases listed.")
        print()
    except Exception as e:
        print(e)


def create_database(name):
    try:
        couchserver = connect_https_couchdb()
        db = couchserver.create(name)
        print(' Database has been created.')
    except Exception as e:
        print(e)


def create_random_databases(numberofdatabases):  # create a random number of databases. good for creating dummy data.
    try:
        i = 0
        while i < numberofdbs:
            couchserver = connect_https_couchdb()
            random_word = get_word(1)
            random_number = random.randint(1000, 100000)
            full_random = f'{random_word}_{random_number}'
            couchserver.create(full_random)
            i += 1
        print(numberofdbs, 'have been created.')
    except Exception as e:
        print(e)


def delete_database(name):
    try:
        couchserver = connect_https_couchdb()
        couchserver.delete(name)
        print(f' Deleted database {name}')
    except Exception as e:
        print(e)


def compact_db(name):
    try:
        couchserver = connect_https_couchdb()
        dumm = couchserver.database(name)
        dumm.compact()
        dumm.cleanup()
        dumm.commit()

    except Exception as e:
        print(e)

#  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv-Document section


def add_document(database_name):  # add a document to named database
    try:
        i = 1
        couchserver = connect_https_couchdb()
        dbname = couchserver.database(database_name)
        gen_sentence = get_sentence(count=50)
        dbname.save({f'name': 'dummdoc', 'data': 'dumdum data for some dumdum to read for a dumdum', 'type': gen_sentence})
        dbname.commit()
        print(f'Document has been added into {dbname}')
    except Exception as e:
        print(e)


def remove_documents(dbname):  # remove all documents from a database.
    try:
        couchserver = connect_https_couchdb()
        ddb = couchserver.database(dbname)
        file_list = ddb.all()
        for x in file_list:
            ddb.delete(x['id'])
        ddb.commit()
        ddb.compact()
        ddb.cleanup()
        print('Documents removed.')
    except Exception as e:
        print(e)


def add_document_with_blob(database_name, filenameforattach):  # add a document with blob
    try:
        couchserver = pycouchdb.Server(db_url)
        dumm = couchserver.database(database_name)
        outgoing_blob = convertToBinaryData(filenameforattach)
        blog_to_ascii = base64.encodebytes(outgoing_blob)
        blob_to_string = blog_to_ascii.decode('ascii')
        enc_blobstring = cryptocode.encrypt(blob_to_string, PASSCODE0)
        attachment1 = convertToBinaryData(filenameforattach)
        attachment1_to_ascii = base64.encodebytes(attachment1)
        attachment1_to_string = attachment1_to_ascii.decode('ascii')
        enc_attachment1 = cryptocode.encrypt(attachment1_to_string, PASSCODE1)
        i = 1
        print('ok')
        while i < 10:
            dumm.save({'name': 'dummy' + str(i), 'attachment1': enc_blobstring, 'attachment2': enc_attachment1})
            dumm.commit()
            print(i)
            i += 1
    except Exception as e:
        print(e)


def get_documents(database_name):
    try:
        couchserver = connect_https_couchdb()
        current_db = couchserver.database(database_name)
        all_docs = list(current_db.all())
        docs_cleaned = []
        for doc in all_docs:
            docs_cleaned.append(doc)
        for docz in docs_cleaned[:5]:  # last 5 documents
            doca1 = docz['doc']['attachment1']
            doca2 = docz['doc']['attachment2']
            doca_name = docz['doc']['name']
            dec_attachment1 = str(cryptocode.decrypt(doca1, PASSCODE0))
            dec_attachment2 = str(cryptocode.decrypt(doca2, PASSCODE1))
            encode_attachment1 = dec_attachment1.encode('ascii')
            encode_attachment2 = dec_attachment2.encode('ascii')
            ascii_str_attachment1 = base64.decodebytes(encode_attachment1)
            ascii_str_attachment2 = base64.decodebytes(encode_attachment2)
            print(doca_name)
            print('orig\t', doca1)
            print()
            print('decoded\t', ascii_str_attachment1)
            print()
    except Exception as e:
        print(e)
    except KeyboardInterrupt as e:
        print('terminated.')


def show_documents(dbname):
    try:
        couchserver = connect_https_couchdb()
        currentdb = couchserver.database(dbname)
        alldocs = list(currentdb.all())
        i = 1
        for doc in alldocs:
            print(f'\t{i}.\t{doc["doc"]["name"] , doc["doc"]["attachment1"][:100]}')  # first 100 chars for attachment1
            i += 1
        alldocs = ''
    except Exception as e:
        print(e)

#  ______________________________________________ Query section


def savequery_db(name):
    try:
        couchserver = connect_https_couchdb()
        dbname = couchserver.database(name)
        _doc = {"_id": "_design/testing", "views": {"names": {"map": "function(doc) { emit(doc.name, 1); }", "reduce": "function(k, v) { return  sum(v); }",}}}
        doc = dbname.save(_doc)
    except Exception as e:
        print(e)


def load_query(name):
    try:
        couchserver = connect_https_couchdb()
        dbname = couchserver.database(name)
        query_data = list(dbname.query("testing/names", group='true'))
        print(query_data)
    except Exception as e:
        print(e)


def convertToBinaryData(filename):
    try:
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    except Exception as e:
        print(e)
