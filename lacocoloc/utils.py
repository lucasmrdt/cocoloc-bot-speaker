import datetime


def debug(action: str, description=None):
    now = datetime.datetime.now()
    if description:
        print(f'[{now.strftime("%d/%m %H:%M")}] {action}: "{description}"')
    else:
        print(f'[{now.strftime("%d/%m %H:%M")}] {action}')
