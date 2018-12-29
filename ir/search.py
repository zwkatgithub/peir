import json
from ir import es
from ir import topics
from ir import final
from ir.query import Query
from ir.result import Result
from ir.config import INDEX, DOC_TYPE, RETURN_SIZE



class Search:
    
    def __init__(self, topic = None):
        if topic is not None:
            self.topic = topics[topic]
            args = [self.topic[name] for name in ('disease', 'gene')]
            self.queryobj = Query(*args)
        #self.create_query()
        #self.__results = self.search()


    def create_query(self, func='query'):
        query = getattr(self.queryobj, func)
        return query

    def _search(self, type):
        query = self.create_query(type)
        #print('here')
        result = es.search(index=INDEX, doc_type=DOC_TYPE, body=query)
        #print('here')
        doc_list = [Result(r["_source"]["doc_id"],r['_score']) for r in result['hits']['hits']]
        return doc_list

    def search(self, type_='auto'):

        result = self._search(type_ if type_!='auto' else 'query')

        if type_=='auto' and len(result) < RETURN_SIZE:
            res = self._search('query_loose')
            result.extend([r for r in res if r not in result])
            if len(result) > RETURN_SIZE:
                result = result[:RETURN_SIZE]
        return result

    def search_by_user(self,disease, gene, type_='auto'):
        self.queryobj = Query(disease, gene)
        return self.search(type_=type_)

    def p(self, results, n=RETURN_SIZE):
        if n == 0:
            raise ValueError('n is 0.')
        c = 0
        for result in results[:n]:
            if final.setdefault((self.topic['number'],result.doc_id), 0) != 0:
                c += 1
        return c / n

        
        


# topic = Topic(r'E:/trec/topics2017.xml')
# for tn in range(0,30):
#     query = Query(topic[tn]['disease'],topic[tn]['gene'],topic[tn]['demographic']).query2()
#     #print(query)
#     with open("./querys/{}.json".format(tn),'w',encoding='utf-8') as f:
#         json.dump(query,f)
#     res = es.search(index=index, doc_type=doc_type, body=query)

#     doc_list = [r["_source"]['doc_id'] for r in res['hits']['hits']]
#     if len(doc_list) < 10:
#         query2 = Query(topic[tn]['disease'],topic[tn]['gene'],topic[tn]['demographic']).query3()
#         res2 = es.search(index=index, doc_type=doc_type, body=query2)
#         doc_list2 = [r["_source"]['doc_id'] for r in res2['hits']['hits']][:10-len(doc_list)]
#         doc_list.extend(doc_list2)
        
#     n = len(doc_list)
#     final = dict()
#     with open('./qrels-final-trials.txt','r',encoding='utf-8') as f:
#         for line in f.readlines():
#             r = line.strip().split(' ')
#             if tn+1 == int(r[0]):
#                 final[r[2]] = int(r[3])
#     c = 0
#     for doc in doc_list:
#         if doc in final.keys() and final[doc] != 0:
#             c+=1
#     print("Topic {} p@{} = {}".format(tn+1,n,c/n if n !=0 else 0))
#     with open('./results/{}.json'.format(tn), 'w', encoding='utf8') as f:
#         json.dump(doc_list,f)
#     # with open("./res.json", 'w', encoding='utf-8') as f:
#     #     json.dump(doc_list, f)