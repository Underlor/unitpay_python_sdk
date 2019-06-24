def insert_url_encode(inserted, params):
    result = ''
    first = True
    for p in params:
        if first:
            first = False
        else:
            result += '&'
        result += inserted + '[' + p + ']=' + str(params[p])
    return result


def remove_signature(params):
    if 'signature' in params:
        del params['signature']
    if 'sign' in params:
        del params['sign']
    return params


def value_list_from_kv_list(data):
    params_list = []
    for p in data:
        params_list.append(str(p[1]))
    return params_list


def dict_to_sorted_kv_list(data):
    """
        Возвращает список ключ-значение словаря отсортированный по ключу
    """
    return [[key, data[key]] for key in sorted(data.keys())]
