from bottle import run, post, request

from main import *


@post('/update')
def post_deal():
    # print(bt_find_by_delivery_code()[0]['ID'])
    # print(get_info_by_id()['UF_CRM_DELIVERY_PRODUCTS'])
    # add_deal(request.json,'products')
    print(valid_delivery_fields())
   #  print(add_products(request.json, 'products'))
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
