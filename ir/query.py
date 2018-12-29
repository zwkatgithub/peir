import json
from ir.expand import Expand
from ir.config import EXPAND_DISEASE_NUM, RETURN_SIZE

class Query:

    def __init__(self, disease, gene):
        
        self.disease = disease
        
        self.gene = Expand.expand_gene(gene)

    @staticmethod
    def _expand_disease2(disease):
        
        diseases = Expand.expand_disease(disease)[:EXPAND_DISEASE_NUM]
        disease_boost = list(range(len(diseases),0,-1))
        res = []
        for dis, boo in zip(diseases, disease_boost):
            if ' ' in dis:
                func = "match_phrase"
            else:
                func = 'match'
            res.extend([
                {
                    func:{"brief_title":{"query":dis, 'boost':boo}}
                },
                {
                    func:{"detail":{"query":dis, 'boost':boo}}
                }
            ]
            )
        return res

    @staticmethod
    def _expand_gene(gene):
        # res = []
        # for g in gene:
        #     res.append({"match":{'summary':g}})
        res = {"match":{"detail":' '.join(g.strip() for g in gene)}}
        return res
    @staticmethod
    def _expand_disease(disease):
        res = []
        res.append({
            "match_phrase":{
                "summary":disease
            }
        })
        return res
    @property
    def query(self):
        if not hasattr(self, '_query'):
            self._query = {
                "query":{
                    "bool":{
                        "must":{
                            "bool":{
                                "should":self._expand_disease2(self.disease),
                                "must":self._expand_gene(self.gene)
                            }
                        },
                       # "should":self._expand_gene(self.gene)
                    }
                },
                'size':RETURN_SIZE
            }
        return self._query
    @property
    def query_loose(self):
        if not hasattr(self, '_query_loose'):
            self._query_loose = {
                "query":{
                    "bool":{
                        "must":{
                            "bool":{
                                "should":self._expand_disease2(self.disease),
                                #"must":self._expand_gene(self.gene)
                            }
                        },
                       "should":self._expand_gene(self.gene)
                    }
                },
                'size':RETURN_SIZE
            }
        return self._query_loose

