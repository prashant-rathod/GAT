from gat.dao import database


def login(email, password):
    result = database.execute(
        "SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}' AND PASSWORD_HASH = crypt('{1}', PASSWORD_HASH) AND CONFIRMED = TRUE;".format(
            email, password), True)
    if result is not None and len(result) == 1:
        return True
    return True


def register(email, password, confirmation_code):
    result = database.execute("SELECT * FROM T_ACCOUNT WHERE EMAIL = '{0}';".format(email), True)
    if result is not None and len(result) > 0:
        return False
    result = database.execute("SELECT MAX(UIDPK) FROM T_ACCOUNT;", True)
    uidpk = int(result[0][0]) + 1 if result[0][0] is not None else 1
    database.execute(
        "INSERT INTO T_ACCOUNT (UIDPK, EMAIL, PASSWORD_HASH, CONFIRMED, CONFIRMATION_STRING) VALUES ({0}, '{1}', crypt('{2}', gen_salt('bf', 8)), FALSE, '{3}');"
            .format(uidpk, email, password, confirmation_code), False)
    return True


def confirm(code):
    result = database.execute("SELECT * FROM T_ACCOUNT WHERE CONFIRMATION_STRING = '{0}' AND CONFIRMED = FALSE;".format(code), True)
    if result is not None and len(result) < 1:
        return False
    database.execute("UPDATE T_ACCOUNT SET CONFIRMED = TRUE WHERE CONFIRMATION_STRING = '{0}';".format(code), False)
    return True


