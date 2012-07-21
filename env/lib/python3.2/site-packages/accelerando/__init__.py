VERSION = (0, 1)

def version():
    return VERSION.join(".")

def release():
    return "0.1"

import accelerando.auth
import accelerando.auth.digest
import accelerando.session

import accelerando.server
