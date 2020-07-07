from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch('http://localhost:9200')

def make_index(es, index_name):
    if es.indices.exists(index = index_name):
        es.indices.delete(index = index_name)
    print(es.indices.create(index = index_name))

index_name = 'goods'
make_index(es, index_name)

doc1 = {'goods_name':'samsung notebook 9', 'price':1000000}
doc2 = {'goods_name':'lg notebook', 'price':2000000}
doc3 = {'goods_name':'apple notebook', 'price':3000000}

es.index(index = index_name, doc_type = 'string', body = doc1)
es.index(index = index_name, doc_type = 'string', body = doc2)
es.index(index = index_name, doc_type = 'string', body = doc3)
es.indices.refresh(index = index_name)

results = es.search(index=index_name, body={'from':0, 'size':10, 'query':{'match':{'goods_name':'notebook'}}})
for result in results['hits']['hits']:
    print('score :', result['_score'], 'source :', result['_source'], 'id : ', result['_id'])

