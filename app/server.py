from bottle import run, post, request

from main import *


@post('/update')
def post_deal():
    try:
        return 'Deal has been added'
    except KeyError:
        return 'Invalid keys'


run(host='localhost', port=8080)
