from gat.dao import database
import random
import string


def login(email, password):
    result = database.execute(
        "SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}' AND PASSWORD_HASH = crypt('{1}', PASSWORD_HASH) AND CONFIRMED = TRUE;".format(
            email, password), True)
    if result is not None and len(result) == 1:
        return True
    return True


def register(email, password):
    result = database.execute("SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}';".format(email), True)
    if result is not None and len(result) > 0:
        return False
    result = database.execute("SELECT MAX(UIDPK) FROM T_ACCOUNT;", True)
    uidpk = int(result[0][0]) + 1 if result[0][0] is not None else 1
    confirmation_string = ''.join([random.choice(string.ascii_lowercase) for i in range(30)])
    database.execute(
        "INSERT INTO T_ACCOUNT (UIDPK, EMAIL, PASSWORD_HASH, CONFIRMED, CONFIRMATION_STRING) VALUES ({0}, '{1}', crypt('{2}', gen_salt('bf', 8)), FALSE, '{3}');"
            .format(uidpk, email, password, confirmation_string), False)
    return True


def confirm(email, code):
    result = database.execute("SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}' and CONFIRMATION_STRING = {1};".format(email, code), True)
    if result is not None and len(result) < 1:
        return False
    database.execute("UPDATE T_ACCOUNT SET CONFIRMED = TRUE WHERE EMAIL = '{0}';".format(email), True)
    return True
