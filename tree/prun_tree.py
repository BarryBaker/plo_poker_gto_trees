# a = {
#     ("2P", True): {
#         ("TP", False): {
#             ("LP", False): {
#                 ("2PT", False): {("SDBL", False): {}},
#                 ("SDBL", False): {
#                     ("SD", False): {("GS1", False): {}, ("OESD1", False): {}, ("OESD", False): {}},
#                     ("MP", False): {},
#                     ("RR", False): {},
#                 },
#                 ("GS", False): {},
#                 ("HRR", False): {},
#                 ("MP", False): {},
#                 ("OESD", False): {},
#                 ("RR", False): {},
#             },
#             ("2PT", False): {
#                 ("SD", False): {("GS1", False): {}, ("OESD", False): {("OESD1", False): {}}, ("SDBL", False): {}},
#                 ("LRR", False): {},
#                 ("RR", False): {("SDBL", False): {}},
#                 ("SDBL", False): {},
#             },
#             ("LRR", False): {},
#             ("OESD", False): {("OESD1", False): {}, ("SDBL", False): {}},
#             ("GS1", False): {},
#             ("SDBL", False): {("GS", False): {}, ("RR", False): {}},
#             ("GS", False): {},
#             ("RR", False): {},
#         },
#         ("SD", False): {
#             ("GS1", False): {("LP", False): {}},
#             ("OESD", False): {
#                 ("LP", False): {("OESD1", False): {}, ("SDBL", False): {}},
#                 ("SDBL", False): {("OESD1", False): {}},
#             },
#             ("LP", False): {("SDBL", False): {}},
#             ("SDBL", False): {},
#         },
#         ("LP", False): {("HRR", False): {("SDBL", False): {}}, ("SDBL", False): {}, ("RR", False): {}},
#         ("SDBL", False): {("RR", False): {}},
#         ("RR", False): {("HRR", False): {}},
#     },
#     ("TRIPS", True): {
#         ("LP", False): {
#             ("MP", False): {
#                 ("SDBL", False): {},
#                 ("2PT", False): {("TRIPS1", False): {}},
#                 ("TRIPS1", False): {},
#                 ("TP", False): {},
#             },
#             ("SDBL", False): {
#                 ("TRIPS1", False): {},
#                 ("SD", False): {("OESD1", False): {}, ("OESD", False): {}, ("GS1", False): {}},
#                 ("TP", False): {},
#             },
#             ("TRIPS1", False): {},
#             ("RR", False): {},
#             ("OESD", False): {},
#             ("GS", False): {},
#             ("TP", False): {},
#         },
#         ("2PT", False): {("TRIPS1", False): {("SDBL", False): {}}, ("SDBL", False): {}},
#         ("OESD", False): {("TRIPS1", False): {("SDBL", False): {("OESD1", False): {}}}, ("OESD1", False): {}},
#         ("GS1", False): {("TRIPS1", False): {}},
#         ("MP", False): {
#             ("TP", False): {("TRIPS1", False): {("SDBL", False): {}}, ("SDBL", False): {}},
#             ("SDBL", False): {("GS", False): {}},
#             ("GS", False): {},
#             ("RR", False): {},
#         },
#         ("GS", False): {("SDBL", False): {}},
#         ("SDBL", False): {("RR", False): {}},
#         ("RR", False): {("LRR", False): {}},
#     },
#     ("SD", False): {
#         ("GS", False): {
#             ("BOP", False): {
#                 ("SDBL", False): {
#                     ("LP", True): {
#                         ("GS1", True): {("RR", False): {("DSDBL", False): {}}},
#                         ("HRR", False): {},
#                         ("RR", False): {},
#                     },
#                     ("LRR", False): {("TP", False): {}},
#                     ("TP", False): {("GS1", False): {("RR", False): {("DSDBL", False): {}}}, ("RR", False): {}},
#                     ("GS1", False): {("DSDBL", False): {}, ("RR", False): {}},
#                     ("RR", False): {},
#                 },
#                 ("LP", False): {("RR", False): {}},
#                 ("TP", False): {("RR", False): {}},
#                 ("RR", False): {},
#             },
#             ("DSDBL", False): {("GS1", False): {}, ("LRR", False): {}},
#             ("SDBL", False): {
#                 ("HRR", False): {("GS1", False): {}},
#                 ("RR", False): {("GS1", False): {}},
#                 ("GS1", False): {},
#             },
#             ("HRR", False): {},
#             ("RR", False): {},
#         },
#         ("BOP", True): {
#             ("MP", False): {
#                 ("HRR", False): {("OESD1", False): {}},
#                 ("SDBL", False): {("OESD1", False): {}, ("OESD", False): {("RR", False): {}}, ("WR1", False): {}},
#                 ("WR", False): {},
#                 ("RR", False): {},
#             },
#             ("LRR", False): {("SDBL", False): {("TP", False): {}}, ("TP", False): {}},
#             ("WR1", False): {("TP", False): {}},
#             ("OESD1", False): {("RR", False): {("TP", False): {}}, ("TP", False): {}},
#             ("RR", False): {("TP", False): {}},
#             ("SDBL", False): {("WR", False): {("TP", False): {}}, ("TP", False): {}},
#             ("OESD", False): {("TP", False): {}},
#             ("TP", False): {},
#         },
#         ("WR", True): {
#             ("SDBL", True): {
#                 ("WR1", False): {("DSDBL", False): {}, ("RR", False): {}},
#                 ("LRR", False): {},
#                 ("RR", False): {},
#             },
#             ("RR", False): {},
#         },
#         ("DSDBL", True): {("OESD1", False): {}},
#         ("SDBL", False): {
#             ("RR", False): {("OESD1", False): {("LRR", False): {}}, ("LRR", False): {}},
#             ("OESD1", False): {},
#         },
#         ("HRR", False): {},
#         ("RR", False): {},
#     },
#     ("BOP", False): {
#         ("SDBL", False): {
#             ("TP", False): {("DSDBL", False): {}, ("HRR", False): {}, ("RR", False): {}},
#             ("LRR", True): {("MP", False): {}},
#             ("DSDBL", False): {("MP", False): {}},
#             ("RR", False): {("MP", False): {}},
#             ("MP", False): {},
#         },
#         ("LRR", False): {("TP", False): {}, ("LP", False): {}},
#         ("RR", False): {("MP", False): {}, ("TP", False): {}},
#         ("LP", False): {("OP", False): {}},
#         ("OP", False): {("TP", False): {}},
#         ("TP", False): {},
#     },
#     ("DSDBL", False): {("LRR", False): {}},
#     ("LRR", False): {("SDBL", False): {}, ("HRR", False): {}},
#     ("SDBL", False): {("RR", False): {}, ("OP", False): {}},
#     ("OP", False): {},
#     ("RR", False): {},
# }


def get_keys(dictionary):
    result = []
    for key, value in dictionary.items():
        result.append(key)
        if type(value) is dict:
            result = result + get_keys(value)

    return result


# print(get_keys(a))


def del_keys(d):
    keylist = list(d.keys())
    for cnt, key in enumerate(keylist):
        approved_right = key[1] or any([j[1] for j in get_keys(d[key])])
        approved_below = False
        if cnt + 1 < len(keylist):
            below = {k: d[k] for k in keylist[cnt + 1 :] if cnt + 1 < len(keylist)}
            approved_below = any([j[1] for j in get_keys(below)])
        if not approved_right and not approved_below:
            del d[key]
        elif type(d[key]) is dict:
            del_keys(d[key])

    # return result


# del_keys(a)
# print(a)


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
    # print(d)
    return replace_keys(d)
