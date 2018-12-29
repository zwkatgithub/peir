import requests

def process_disease(disease):
    return disease.lower().replace("cancer",'').replace('neoplasm','').strip()

class Expand:
    wikisynonyms_api = 'http://wikisynonyms.ipeirotis.com/api/{term}'
    MAX_AGE = 10000
    MIN_AGE = -1
    @classmethod
    def expand_disease(cls, disease):
        result = requests.get(cls.wikisynonyms_api.format(term=disease))
        if result.text == '':
            nd = disease.split()[0] + ' cancer'
            result = requests.get(cls.wikisynonyms_api.format(term=nd))
        res = result.json()
        if res['http'] != 200:
            raise ValueError(disease)
        best = res['terms'][0]['term']
        terms = [process_disease(best)]
        if process_disease(disease) not in terms:
            terms.append(process_disease(disease))
        #terms.union(set([term['term'].replace('cancer','').replace('Cancer','').strip() for term in res['terms']]))
        terms.extend([process_disease(term['term']) for term in res['terms'] if process_disease(term['term']) not in terms])
        return terms
    @staticmethod
    def expand_gene(gene):
        
        return gene.replace('(','').replace(')',"").strip().split(',')


        
    