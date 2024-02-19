def count(prod, c=0, importance_list=[]):
    for mykey in prod:
        if isinstance(prod[mykey], dict):
            c, importance_list = count(prod[mykey], c + 1, importance_list + [mykey[2]])
    return c, importance_list


def get_keys(dictionary):
    result = []
    for key, value in dictionary.items():
        result.append(key)
        if type(value) is dict:
            result = result + get_keys(value)

    return result


# print(get_keys(a))


def del_keys(d, imp=0):
    keylist = list(d.keys())
    for cnt, key in enumerate(keylist):
        approved_right = (key[1] and key[2] > imp) or any(
            [(j[1] and j[2] > imp) for j in get_keys(d[key])]
        )
        approved_below = False
        if cnt + 1 < len(keylist):
            below = {k: d[k] for k in keylist[cnt + 1 :] if cnt + 1 < len(keylist)}
            approved_below = any([(j[1] and j[2] > imp) for j in get_keys(below)])
        if not approved_right and not approved_below:
            del d[key]
        elif type(d[key]) is dict:
            del_keys(d[key], imp)


# def del_keys(d):
#     keylist = list(d.keys())
#     for cnt, key in enumerate(keylist):
#         approved_right = key[1] or any([j[1] for j in get_keys(d[key])])
#         approved_below = False
#         if cnt + 1 < len(keylist):
#             below = {k: d[k] for k in keylist[cnt + 1 :] if cnt + 1 < len(keylist)}
#             approved_below = any([j[1] for j in get_keys(below)])
#         if not approved_right and not approved_below:
#             del d[key]
#         elif type(d[key]) is dict:
#             del_keys(d[key])

# return result


def replace_keys(d):
    new_dict = {}
    for key in d.keys():
        new_key = key[0]
        if isinstance(d[key], dict):
            new_dict[new_key] = replace_keys(d[key])
        else:
            new_dict[new_key] = d[key]

    return new_dict


def pruin_tree(d):
    del_keys(d)

    keycount, importances = count(d)
    importances.sort()
    print(importances)
    # if keycount > 55:

    #     importances.sort()
    #     idx = max(keycount - 59, 0)
    #     while keycount > 55:
    #         del_keys(d, importances[idx])
    #         keycount, _ = count(d)
    #         idx += 1

    return replace_keys(d)
