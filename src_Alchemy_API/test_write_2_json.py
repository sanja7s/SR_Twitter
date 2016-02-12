import demjson



d1 = {u'books and literature': {u'poetry': {'size': 1.381699}}, \
    u'humor': {'size': 4.859961}, u'theatre': {u'theatre awards':  {'size': 0.40856}}}


d2 = { 
    "books and literature": { 
        "poetry": { 
            "size": 1.381699 
        } 
    }, 
    "comics and animation": { 
        "anime and manga": { 
            "size": 0.577505 
        }, 
        "comics": { 
            "size": 0.318583 
        },
        "size": 0.778583
    } 
    }


d3 = 

def recursive_writeable_json_from_dict(d):

    # stop criteria: len(d) == 1 means this is a leaf 
    # (should not allow here to arrive, for example { "size": 1.381699 }  )
    # only, for example { "poetry": { "size": 1.381699 } }
    if len(d) == 1:
        s = {}
        #print d, d.items()[0][1], d.items()[0][0]
        s["size"] = d.items()[0][1]["size"]
        s["name"] = d.items()[0][0]
        #print s["name"]
        return s
    # recursive criteria satisfied: create a new dict
    # add me my children, since I have
    #s = {}
    #s["children"] = []
    s = []
    for child_k in d.keys():
        if child_k == "size":
            #s["size"] = d[child_k]
            s.append({"size":d[child_k]})
        else:
            child_el = d[child_k]
            ss = {"name": child_k}
            try:
                ss["size"] = child_el["size"]
            except: KeyError
            # this is a check to avoid passing { "size": 1.381699 } 
            #if child_el.items()[0][0] == "size" and len(child_el) == 1:
            #    s["children"].append()
            #    continue
            #print child_el
            #if len(child_el) > 1: 
                #ss["children"] = recursive_writeable_json_from_dict(child_el)
            if child_el.items()[0][0] == "size" and len(child_el) == 1:
                #s["children"].append(ss)
                s.append(ss)
                continue
            ss["children"] = recursive_writeable_json_from_dict(child_el)
            #s["children"].append(ss)
            s.append(ss)

    return s




print recursive_writeable_json_from_dict(d2)

res7s = recursive_writeable_json_from_dict(d2)

json7s = demjson.encode(res7s)

print json7s