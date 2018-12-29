from ir import final

def format_results(topic, results, n, p):
    res = []
    for result in results[:n]:
        d = dict(
                {
                    "doc_id": result.doc_id,
                    "score": result.score,
                }
            )
        if topic is not None:
            d['tag'] = final.setdefault((topic + 1, result.doc_id), 0)
        res.append(d)
    return res