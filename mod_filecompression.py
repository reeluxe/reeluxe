import gzip


def compress_file(filename):
    filename_clean = str(filename)
    try:
        file_input = open(filename_clean, 'rb')
        compressed_filename = filename + '.gz'
        s = file_input.read()
        file_input.close()
        output = gzip.GzipFile(compressed_filename, 'wb')
        output.write(s)
        output.close()
        return s
    except Exception as e:
        print(e)


def decompress_file(filename):
    try:
        orig_filename, old_ext = filename.split('.gz')
        file_input = gzip.GzipFile(filename, 'rb')
        s = file_input.read()
        file_input.close()
        output = open(orig_filename, 'wb')
        output.write(s)
        output.close()
        return s
    except Exception as e:
        print(e)


def compress_data(data):
    try:
        bdata = bytes(data, 'utf8')
        comp_data = gzip.compress(bdata)
        print(comp_data)
        return comp_data
    except Exception as e:
        print(e)


def decompress_data(data):
    try:
        dcomp_data = gzip.decompress(data)
        return dcomp_data
    except Exception as e:
        print(e)
