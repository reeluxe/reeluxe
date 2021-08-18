import io

from minio import Minio
# For self signed certs use "export env var SSL_CERT_FILE="/etc/minio/certs/public.crt" "


def minio_server_connect():
    try:
        client = Minio(endpoint="192.168.1.211:8080", access_key="minio", secret_key="miniostorage", secure=True)
        return client
    except Exception as e:
        print(e)


def minio_get_buckets():
    try:
        client = minio_server_connect()
        bucketlist = client.list_buckets()
        bucket_count = len(bucketlist)
        print(f'Found {bucket_count} buckets on {client}')
        for bucket in bucketlist:
            print(bucket)
    except Exception as e:
        print(e)


def minio_create_bucket():
    try:
        client = minio_server_connect()
        name = input("New name of Bucket: ")
        client.make_bucket(bucket_name=name)
        print(f'{name} bucket has been created.')
    except Exception as e:
        print(e)


def minio_send_object(bucket_name_input):
    try:
        client = minio_server_connect()
        send_object = 'screenshot_compressed.jpg'
        blobdata = convertToBinaryData(send_object)
        blob_length = len(blobdata)
        client.put_object(bucket_name_input, send_object, io.BytesIO(blobdata), blob_length)
    except Exception as e:
        print(e)


def minio_show_objects(bucket_name_input):
    try:
        client = minio_server_connect()
        bucket_objects = client.list_objects(bucket_name_input, recursive=True)
        i = 0
        for countitem in bucket_objects:
            i += 1
        bucket_objects_count = i
        print(f'{bucket_objects_count} objects found.\n')
        for item in bucket_objects:
            print(item.object_name.encode('utf-8'))
    except Exception as e:
        print(e)


def convertToBinaryData(filename):
    try:
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    except Exception as e:
        print(e)

