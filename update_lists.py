#!/usr/bin/env python

# title        :update_lists.py
# description  :download multiple lists and make a single result list
# author       :Daniel Fuentes B.
# date         :08-06-2014
# version      :0.1
# licence      :MIT License/X11 license (see COPYING.txt file)
# usage        :python update_lists.py
# ===================================================================

########### START EDIT HERE ###########

# Level 1, Borgon and Spyware list from Bluetack (.zip files)
# Add or remove lists, as you wish (only in p2p format and .zip files)

urls = ["http://list.iblocklist.com/?list=ydxerpxkpcfqjaybcssw&fileformat=p2p&archiveformat=zip",
    "http://list.iblocklist.com/?list=gihxqmhyunbxhbmgqrla&fileformat=p2p&archiveformat=zip",
    "http://list.iblocklist.com/?list=llvtlsjyoyiczbkjsxpf&fileformat=p2p&archiveformat=zip" ]

# Name of the final list (output list)

ouputlistname = "listas.p2p"

########### STOP EDIT HERE ############

# ===================================================================
# import modules
# ===================================================================

import os.path
import os
import shutil
import urllib
import zipfile

# ===================================================================
# class and funtions
# ===================================================================


class MyOpener(urllib.FancyURLopener):
    """change the python/urllib user agent"""
    # By default python use: URLopener.version = "Python-urllib/1.xx"
    version = "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)"


def create_dir(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            if not os.path.isdir(path):
                raise
    else:
        pass

def delete_dir(directory):
    shutil.rmtree(directory)

def download_file(URL, filename):
    # Cambiamos el user agent por el definido anteriormente:
    urlretrieve = MyOpener().retrieve
    f = urlretrieve(URL, filename)

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)


# ===================================================================
# Main program:
# ===================================================================


if __name__ == "__main__":
    #creamos un directorio temporal para trabajar, llamado "temp0001"
    temp_dir = os.path.join(os.curdir, "temp0001")
    create_dir(temp_dir)
    # descargamos los .ZIP con las listas y los descomprimimos
    for lists in urls:
        try:
            zipfilename = os.path.join(temp_dir, "temp.zip")
            myopener = MyOpener()
            myopener.retrieve(lists, zipfilename)
            unzip(zipfilename, temp_dir)
        # Mensaje en caso de error o de no encontrarse la ruta
        except:
            print "Error: Failed to obtain information"
    
    # se buscan todas las listas y unen en un solo archivo
    listfilenames = []
    for file in os.listdir(temp_dir):
        if file.endswith(".txt"):
            listfilenames.append(str(file))
        if file.endswith(".p2p"):
            listfilenames.append(str(file))
        else:
            pass
    if os.path.exists(os.path.join(os.curdir, ouputlistname)):
        #se sobrescribe el archivo existente
        print "yes"
        f = open(os.path.join(os.curdir, ouputlistname), "w")
        f.write("")
        f.close()
    else:
        f = open(os.path.join(os.curdir, ouputlistname), "w")
        f.close()
    print listfilenames
    # se agregan las listas a la principal
    for elemento in listfilenames:
        # archivo origen
        inputfile = open(os.path.join(temp_dir, elemento), "r")
        # archivo destino
        outputfile = open(os.path.join(os.curdir, ouputlistname), "a")
        # se escribe en el destino una a una las lines del origen
        linea = inputfile.readline()
        while linea != "":
            outputfile.write(linea)
            linea = inputfile.readline()
        inputfile.close()
        outputfile.close()
    
    # se elimina el directorio temporal
    delete_dir(temp_dir)
