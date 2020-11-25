import jwt

import my_settings


def getValueFromToken(token, key):
    user_data   = jwt.decode(token, my_settings.SECRET['secret'], algorithm=my_settings.ALGORITHM['hash'])

    return user_data[key]

