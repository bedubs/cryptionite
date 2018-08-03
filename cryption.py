import os

import pyAesCrypt

bufferSize = 64 * 1024


def encrypt(file, password):
    encrypted_file = f"{file}.aes"
    pyAesCrypt.encryptFile(file, encrypted_file, password, bufferSize)
    return encrypted_file


def decrypt(new_file, file, password):
    new_file = os.path.join(os.getcwd(), new_file)
    pyAesCrypt.decryptFile(file, new_file, password, bufferSize)
    return new_file
