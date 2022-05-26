from bottle import run, post, request

from main import *


@post('/update')
def post_deal():
    # try:
    #     print(valid_contact())
    #     "Операция совершена успешно"
    # except KeyError:
    #     return "Проверьте правильность введеных данных"
    # # print(update_contact())
    print(valid_delivery_code())
run(host='localhost', port=8080)
