# from time import sleep
# from datetime import datetime

from bottle import request
from fast_bitrix24 import Bitrix




###------------------------------------  ---  ---START HERE---  ---  ------------------------------------------------###
webhook = 'https://b24-xlxcp4.bitrix24.ru/rest/1/tscp6l1psv3emwmq/'
b = Bitrix(webhook)


def add_products(data, k):  # ---return products from request
    products_list = []
    for product in data[k]:
        products_list.append(product)
    return products_list


def check_number(data, k):  # ---return number from request
    return data[k]


def add_contact(data):
    contact_fields = b.call(
        'crm.contact.add',
        {
            'CONTACT_ID': 'ID',
            'fields': {
                'NAME': data['contact']['name'],
                'LAST_NAME': data['contact']['surname'],
                "TYPE_ID": "CLIENT",
                'PHONE': [{'VALUE': data['contact']['phone']}],
                'ADDRESS': data['contact']['address']
            }
        }

    )
    return contact_fields


def add_deal(data, k):
    b.call(
        'crm.deal.add',
        # 'crm.contact.fields',
        {
            'fields': {
                'ADDITIONAL_INFO': data['description'],
                'TITLE': data['title'],
                'UF_CRM_DELIVERY_CODE': data['delivery_code'],
                'UF_CRM_DELIVERY_PRODUCTS': add_products(data, k),
                'UF_CRM_DELIVERY_ADDRESS': data['delivery_address'],
                'UF_CRM_DELIVERY_DATE': data['delivery_date'],
                'CONTACT_ID': add_contact(data)
            }
        }
    )


def valid(x, y):
    return x in y


def test():
    d = request.json['contact']
    d = {'NAME': d['name'], 'LAST_NAME': d['surname'], 'ADDRESS': d['address']}
    return d


def check_contact():
    pin = request.json['contact']
    return pin


def get_contacts_list():
    pass


def bt_get_phone(data):
    b.call('crm.duplicate.findbycomm',
    {
        'ENTITY_TYPE': "CONTACT",
        'TYPE': "PHONE",
        'VALUES': [request.json['contact']['phone']],
    })
    return True


bt_contact_list = b.call('crm.contact.list',
                         {
                             'FILTER': ['*'],
                             'SELECT': ['NAME', 'LAST_NAME', 'ADDRESS', 'PHONE']
                         }
                    )



def start():
    if not bt_get_phone(request.json['contact']):
        return add_contact(request.json)


# phones_duplicate = b.call(
#             'crm.duplicate.findbycomm',
#             {
#                 'ENTITY_TYPE': "CONTACT",
#                 'TYPE': "PHONE",
#                 'VALUES': 'PHONE'
#             })


# contact_list = b.list_and_get(
#     'crm.contact.fields',
#     'ID'
#
# )


deals = b.get_all('crm.deal.list')

nums = b.get_by_ID('crm.deal.contact.items.get',
                   [d['ID'] for d in deals])


###------------------------------------    Main() Starter Function    -----------------------------------------------###
# if __name__ == '__main__':
#     while True:
#         now = datetime.now()
#         print(now.hour)
#         if now.hour == 6 or now.hour == 22:
#             main()
#         sleep(1)

###------------------------------------    Another functions    -----------------------------------------------------###


def add_users_field():  # ---add users field by fields
    b.call(
        'crm.deal.userfield.add',
        {
            'fields': {
                'ID': 'contact_surname_field',
                "FIELD_NAME": "contact_surname",
                "EDIT_FORM_LABEL": "Фамилия контакта",
                "LIST_COLUMN_LABEL": "Фамилия контакта",
                "USER_TYPE_ID": "string",
                "XML_ID": "MY_STRING",
                "SETTINGS": {"DEFAULT_VALUE": 'None'},
                'MULTIPLE': 'N'
            }
        }
    )
    return True

# def update_deal_by_field(pk, data):           #TODO доделать
#
#     b.call(
#         'crm.deal.update',
#         {
#             'ID': pk,
#             'fields': {
#                 'UF_CRM_DELIVERY_CODE': data['delivery_code'],
#                 'desc': data["description"],
#                 'contact': data['client'{
#
#                 }]
#     }
#     }
#     )
#     return data['delivery_code']


# 'crm.deal.list',                          #TODO доделать
# params={
#     'select': ['*', 'UF_*'],
#     'filter': {'CONTACT': 'PHONE'}
# })
