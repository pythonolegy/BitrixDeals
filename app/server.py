from bottle import run, post, request

from main import *


@post('/update')
def post_deal():
    valid_contact()
    # print(bt_get_phone())
    return 'ok'

# @post('/update')
# def post_deal():
#     try:
#         if not valid_contact():
#             return 'contact is already exist'
#         valid_contact()
#         return 'contact has been added'
#     except KeyError:
#         return 'Invalid keys'


run(host='localhost', port=8080)
