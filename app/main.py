from bottle import request
from fast_bitrix24 import Bitrix

###------------------------------------  ---  ---START HERE---  ---  ------------------------------------------------###

webhook =    # персональный вебхук Bitrix24
b = Bitrix(webhook)  # переменная-сокращение для вызова методов 'b.call()'


def add_products():
    """ Добавление в список продукты из запроса с ключом 'products'
       *Функция возвращает список 'products_list' """
    products_list = []
    for product in request.json['products']:
        products_list.append(product)
    return products_list


def add_deal_link_contact():
    """Добавление сделки с полями 'fields' из запроса
    *В случае наличия контакта, связывает сделку и контакт"""
    b.call(
        'crm.deal.add',
        {
            'fields': {
                'TITLE': request.json['title'],
                'UF_CRM_DELIVERY_CODE': request.json['delivery_code'],
                'UF_CRM_DELIVERY_PRODUCTS': add_products(),
                'UF_CRM_DELIVERY_ADDRESS': request.json['delivery_address'],
                'UF_CRM_DELIVERY_DATE': request.json['delivery_date'],
                'CONTACT_ID': bt_get_phone_duplicate()['CONTACT'][0]
            }
        }
    )


def add_contact():
    """Добавление контакта с полями 'fields' из запроса"""
    contact_fields = b.call(
        'crm.contact.add',
        {
            'fields': {
                'NAME': request.json['contact']['name'],
                'LAST_NAME': request.json['contact']['surname'],
                "TYPE_ID": "CLIENT",
                'PHONE': [{'VALUE': request.json['contact']['phone']}],
                'ADDRESS': request.json['contact']['address']
            }
        }
    )
    return contact_fields


def add_contact_to_deal():
    """
    Добавление контакта в сделку
        * 'id': 'ID' сделки
        * 'CONTACT_ID': 'ID' контакта
    """
    b.call(
        'crm.deal.contact.add',
        {
            'id': get_info_by_id()['ID'],
            'fields': {
                'CONTACT_ID': bt_get_phone_duplicate()['CONTACT'][0]
            }
        }
    )


def update_delivery_fields():
    """
    Обновление полей 'fields' сделки
        * 'FIELD_NAME': str
        * 'id': 'ID' сделки
    """
    b.call(
        'crm.deal.update',
        {
            'id': get_info_by_id()['ID'],
            'fields': {
                'UF_CRM_DELIVERY_ADDRESS': request.json['delivery_address'],
                'UF_CRM_DELIVERY_DATE': request.json['delivery_date'],
                'UF_CRM_DELIVERY_PRODUCTS': add_products()
            }
        }
    )


def bt_get_phone_duplicate():
    """
    Поиск дубликата по номеру телефона контакта из запроса
        * Функция возвращает номер телефона
    """
    x = b.call('crm.duplicate.findbycomm',
               {
                   'ENTITY_TYPE': "CONTACT",
                   'TYPE': "PHONE",
                   'VALUES': [request.json['contact']['phone']],
               })
    return x


def bt_find_by_delivery_code():
    """
        Поиск дубликата по номеру заявки из запроса
            * Функция возвращает поля и значения полей сделки со значением номера заявки
    """
    x = b.call('crm.deal.list',
               {
                   'FILTER': {'UF_CRM_DELIVERY_CODE': request.json['delivery_code']}
               })
    return x


def get_info_by_id():
    """  * Функция со значением аналогичным 'bt_find_by_delivery_code()', иного вида, с использованием другого метода
         * используется во избежание некоторых пересечений"""
    x = b.call(
        'crm.deal.get',
        {'ID': bt_find_by_delivery_code()[0]['ID']}
    )
    return x


def valid_delivery_code():
    """
    Функция проверка на совпадение номера заявки
        * Если код заявки есть, возвращает True или False
        * Используется для логической расстановки инструкций в функции 'main()'
    """
    try:
        return request.json['delivery_code'] == valid_get_info_by_id()['UF_CRM_DELIVERY_CODE']
    except TypeError:
        return False


def valid_get_info_by_id():
    """Функция, аналогичная по использованию функции 'valid_delivery_code()', возвращает True или False"""
    try:
        return get_info_by_id()
    except:
        return False


def valid_delivery_fields():
    """
        Функция, аналогичная по использованию функции 'valid_delivery_code()',
        * Проверяется совпадают ли указанные поля сделки с полями в запросе
        * возвращает True или False
        """
    try:
        a, p = request.json['delivery_date'], request.json['delivery_address']
        c, d = get_info_by_id()['UF_CRM_DELIVERY_DATE'], get_info_by_id()['UF_CRM_DELIVERY_ADDRESS']
        e, f = add_products(), get_info_by_id()['UF_CRM_DELIVERY_PRODUCTS']
        return a == c and p == d and e == f
    except IndexError:
        return False


def main():
    """ Главная функция, запускаемая из файла 'server.py' с методом 'POST' """
    if not bt_get_phone_duplicate():
        add_contact()
        if not valid_delivery_fields():
            add_deal_link_contact()
            return 'Сделка и контакт созданы'
        add_contact_to_deal()
        return "Контакт создан, сделка с таким номером заявки уже существует, проверьте номер заявки"
    elif bt_get_phone_duplicate():
        if not valid_delivery_code():
            add_deal_link_contact()
            return 'Контакт обнаружен, объединение со сделкой'
        elif valid_delivery_code():
            if not valid_delivery_fields():
                update_delivery_fields()
                return 'Сделка обновлена'
    return 'Изменений не обнаружено'


###-------------------------------------- -- Finish - Here --  ------------------------------------------------------###
