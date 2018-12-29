import os
import json
from elasticsearch import Elasticsearch
from ir.config import INDEX, DOC_TYPE
from ir.topic import Topic
from ir.secure import HOST, PORT


path, _ = os.path.split(__file__)

with open(os.path.join(path,'settings.json'),'r',encoding='utf-8') as f:
    settings = json.load(f)

server = [{'host':HOST,'port':PORT}]

es = Elasticsearch(server)

if es.indices.exists(index=INDEX) is not True:
    es.indices.create(index=DOC_TYPE, body=settings)

final = dict()

with open(os.path.join(path, 'data','qrels-final-trials.txt'),'r',encoding='utf-8') as f:
    for line in f.readlines():
        r = line.strip().split(' ')
        final[(int(r[0]),r[2])] = int(r[3])

topics = Topic(os.path.join(path, 'data','topics2017.xml'))
