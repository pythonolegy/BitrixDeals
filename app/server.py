from bottle import run, post, request

from main import *


@post('/update')
def post_deal():
    print(valid_contact())
    # print(bt_get_phone_duplicate())

run(host='localhost', port=8080)
