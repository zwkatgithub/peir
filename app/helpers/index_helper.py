from ir import topics

def format_topics(n):
    res = []
    for i in range(6):
        t = []
        for j in range(i * 5, (i + 1) * 5):
            t.append({'number': topics[j]['number'], 'href': 'search/{}/{}'.format(j, n)})
        res.append(t)
    return res

def choice2str(c):
    if c == 0:
        return 'auto'
    elif c == 1:
        return 'query'
    elif c== 2:
        return 'query_loose'
    else:
        raise ValueError(c)