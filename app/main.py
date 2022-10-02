from bottle import request
from fast_bitrix24 import Bitrix

webhook = 'example'  # Bitrix24 personal webhook
b = Bitrix(webhook)  # variable-abbreviation for calling methods 'b.call()'


def add_products():
    """ Adding products from a request with the 'products' key to the list
       *The function returns a list of 'products_list' """
    products_list = []
    for product in request.json['products']:
        products_list.append(product)
    return products_list


def add_deal_link_contact():
    """ Adding a transaction with 'fields' fields from the request
        *If there is a contact, connects the transaction and the contact """
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
    """ Adding a contact with 'fields' fields from a request """
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
    Adding a contact to a deal
        * 'id': 'ID' of the transaction
        * 'CONTACT_ID': 'ID' of the contact
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
    Updating the 'fields' of the transaction
        * '* 'FIELD_NAME': string
        * 'id': 'ID' of the transaction
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
    Search for a duplicate by the contact's phone number from the request
        * The function returns the phone number
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
    Search for a duplicate by the application number from the request
        * The function returns the fields and values of the transaction fields with the value of the order number
    """
    x = b.call('crm.deal.list',
               {
                   'FILTER': {'UF_CRM_DELIVERY_CODE': request.json['delivery_code']}
               })
    return x


def get_info_by_id():
    """
        * A function with a value similar to 'bt_find_by_delivery_code()', of a different type, using a different method
        * used to avoid some intersections """
    x = b.call(
        'crm.deal.get',
        {'ID': bt_find_by_delivery_code()[0]['ID']}
    )
    return x


def valid_delivery_code():
    """
    The function check for a match of the application number
        * If there is a request code, returns True or False
        * Used for logical placement of instructions in the 'main()' function
    """
    try:
        return request.json['delivery_code'] == valid_get_info_by_id()['UF_CRM_DELIVERY_CODE']
    except TypeError:
        return False


def valid_get_info_by_id():
    """ A function similar to using the 'valid_delivery_code()' function returns True or False """
    try:
        return get_info_by_id()
    except:
        return False


def valid_delivery_fields():
    """
    A function similar to using the 'valid_delivery_code()' function,
        * Checks whether the specified transaction fields match the fields in the request
        * returns True or False
    """
    try:
        a, p = request.json['delivery_date'], request.json['delivery_address']
        c, d = get_info_by_id()['UF_CRM_DELIVERY_DATE'], get_info_by_id()['UF_CRM_DELIVERY_ADDRESS']
        e, f = add_products(), get_info_by_id()['UF_CRM_DELIVERY_PRODUCTS']
        return a == c and p == d and e == f
    except IndexError:
        return False


def main():
    """ The main function launched from the file 'server.py ' with the 'POST' method """
    if not bt_get_phone_duplicate():
        add_contact()
        if not valid_delivery_fields():
            add_deal_link_contact()
            return 'Deal and contact created'
        add_contact_to_deal()
        return 'A contact has been created, a deal with such an application number already exists, check the application number'
    elif bt_get_phone_duplicate():
        if not valid_delivery_code():
            add_deal_link_contact()
            return 'Contact detected, merge with transaction'
        elif valid_delivery_code():
            if not valid_delivery_fields():
                update_delivery_fields()
                return 'Deal updated'
    return 'No changes detected'
