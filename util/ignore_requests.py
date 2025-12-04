IGNORE_TOKEN_VERIFICATION_ENDPOINTS = ['/user-service/auth/login',
                                       '/user-service/users',
                                       '/user-service/ping',
                                                                                          '/user-service/users/organizations']


def check_ignore_token(path, method):
    if method == 'OPTIONS':
        return True

    if IGNORE_TOKEN_VERIFICATION_ENDPOINTS.__contains__(path):
        return True
    if 'geo' in path:
        return True
    return False
