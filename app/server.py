from bottle import run, post, request

from main import *


@post('/update')
def post_deal():
    try:
        add_deal(request.json, 'products')
        # print(check_number(request.json['contact'], 'phone'))
        return 'Deal has been added'
    except KeyError:
        return 'Invalid keys'


run(host='localhost', port=8080)

