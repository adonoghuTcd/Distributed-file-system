"""
Constants used in order to allow consistent messages passed accross file system
"""


def DATABASE():
    return "sql.db"


def open_file(file):
    return "OPEN${}".format(file)


def lock_file(file):
    return "LOCK${}".format(file)


def check_if_locked(file):
    return "CHECK${}".format(file)


def get_file_meta(file_name):
    return "GET${}".format(file_name)


def insert_file_meta(file):
    return "ADD${}".format(file)

def response405():
    response = "405 path not found"
    return response


def response404():
    response = "404 file not found"
    return response


def response200():
    return "200 OK"


def response604():
    return "604 file not locked"


def response605():
    return "605 unable to unlock file, it may not be locked"


def responseErrParse():
    return "could not parse!"


def responseLocked():
    return "file@locked"


def responseUnlocked():
    return "file@unlocked"


def dirExists():
    return "Directory exists"
