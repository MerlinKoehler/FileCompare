# first argument: file path


# class file: filename, filepath, filesize, filehash, created, lastmodified, lastaccessed, filetype
from datetime import datetime
import hashlib
import os


class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.filesize = os.path.getsize(filepath)
        self.filehash = self.gethash(filepath)
        self.created = datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        self.lastmodified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        self.lastaccessed = datetime.fromtimestamp(os.path.getatime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        self.filetype = os.path.splitext(filepath)[1]

    def gethash(self, filepath):
        h  = hashlib.sha256()
        b  = bytearray(128*1024)
        mv = memoryview(b)
        with open(filepath, 'rb', buffering=0) as f:
            while n := f.readinto(mv):
                h.update(mv[:n])
        return h.hexdigest()



import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python scanpath.py <file path>")
        sys.exit(1)
    path = sys.argv[1]
    files = []
    for root, dirs, filenames in os.walk(path):
        for f in filenames:
            filepath = os.path.join(root, f)
            print(filepath)
            files.append(File(filepath))

    # save files to csv file
    seperator = ";"
    with open('files.csv', 'w') as f:
        f.write("Filename" + seperator + "Filepath" + seperator + "Filesize" + seperator + "Filehash" + seperator + "Created" + seperator + "Lastmodified" + seperator + "Lastaccessed" + seperator + "Filetype" + "\r")
        for file in files:
              f.write(file.filename + seperator + file.filepath + seperator + str(file.filesize) + seperator + file.filehash + seperator + file.created + seperator + file.lastmodified + seperator + file.lastaccessed + seperator + file.filetype + "\r")

if __name__ == '__main__':
    main()