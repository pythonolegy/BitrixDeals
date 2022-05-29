from bottle import run, post

from main import main


@post('/update')
def post_deal():
    try:
        return main()
    except KeyError:
        return 'Проверьте введенные данные'


run(host='localhost', port=8080)
