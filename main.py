import config
import json
import datetime


def print_operation_info(operation):
    date = datetime.datetime.strptime(operation['date'], config.DATE_FORMAT)
    card = operation.get('from')
    str_card = ''
    if card:
        card_type, card_num = card[:-16], card[-16:]
        str_card = f'{card_type} {card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}'

    print(f'''{date.strftime('%d.%m.%Y')} {operation['description']}
{str_card} -> {operation['to']}
{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}
''')


def get_last_operation():
    with open(config.OPERATIONS_FILE_PATH, 'r', encoding='utf-8') as operations_json:
        operations: list = json.load(operations_json)
        operations = list(filter(lambda x: bool(x) and x.get("state") == 'EXECUTED', operations))
        operations.sort(
            key=lambda value: datetime.datetime.strptime(value['date'], config.DATE_FORMAT),
            reverse=True
        )
        list(map(print_operation_info, operations[:config.WINDOW_SIZE]))


get_last_operation()
