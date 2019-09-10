import time
import json as json
import re
import sys
import os
from collections import defaultdict
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

INDEX_NAME = "icd11"
NUMBER_SHARDS = 1 # keep this as one if no clusterNUMBER_REPLICAS = 0
NUMBER_REPLICAS = 0

request_body = {
        "settings": {
            "number_of_shards": NUMBER_SHARDS,
            "number_of_replicas": NUMBER_REPLICAS
        },
        "mappings": {
                "properties": {
                    "id": {
                        "type": "keyword"
                    },
                    "tree":{
                        "type": "text"
                    },
                    "name":{
                        "type": "text"
                    },
                    "root":{
                        "type": "text"
                    },
                    "degree":{
                        "type": "integer"
                    },
                    "definition":{
                        "type": "text"
                    },
                    "synonym":{
                        "type": "text"
                    }
                }
            }
        }


es = Elasticsearch()

if es.indices.exists(INDEX_NAME):
     res = es.indices.delete(index = INDEX_NAME)
     print("Deleting index %s , Response: %s" % (INDEX_NAME, res))

res = es.indices.create(index = INDEX_NAME, body = request_body)
print("Create index %s , Response: %s" % (INDEX_NAME, res))
DATA = None
with open("DATA.json", 'r')as f2:
    DATA= json.load(f2)

logFilePath = "log.txt"

INDEX_NAME = "icd11"

es = Elasticsearch()

ic = 0
ir = 0

with open(logFilePath, "w") as fout:
        start = time.time()
        bulk_size = 50 # number of document processed in each bulk index
        bulk_data = [] # data in bulk index

        cnt = 0
        for item in DATA: ## each item is single document
                cnt += 1
                
                data_dict = {}
                
                # update ID
                data_dict["id"] = item["id"]
                
        

                # update detail<------------------
                data_dict["tree"] = item["tree"]
                data_dict["root"] = item["root"]
                data_dict["name"] = item["name"]
                data_dict['parents']=item['parents']
                data_dict['childs'] = item['childs']
                data_dict["sibls"] = item["sibls"]
                data_dict["degree"] = item["degree"]
                data_dict["synonym"] = item["synonym"]
                data_dict["definition"] = item["definition"]

                        
                
                ## Put current data into the bulk <---------
                op_dict = {
                    "index": {
                        "_index": INDEX_NAME,
                        "_id": data_dict["id"]
                    }
                }

                bulk_data.append(op_dict)
                bulk_data.append(data_dict) 
                
                
                
                        
                ## Start Bulk indexing
                if cnt % bulk_size == 0 and cnt != 0:
                    ic += 1
                    tmp = time.time()
                    es.bulk(index=INDEX_NAME, body=bulk_data, request_timeout = 500)
                    fout.write("bulk indexing... %s, escaped time %s (seconds) \n" \
                               % ( cnt, tmp - start ) )
                    
                    if ic%50 ==0:
                        print(" i bulk indexing... %s, escaped time %s (seconds) " \
                              % ( cnt, tmp - start ) )
                    
                    
                    bulk_data = []
                
                
        
        ## indexing those left papers
        if bulk_data:
            ir +=1
            tmp = time.time()
            es.bulk(index=INDEX_NAME, body=bulk_data, request_timeout = 500)
            fout.write("bulk indexing... %s, escaped time %s (seconds) \n"\
                       % ( cnt, tmp - start ) )
            
            if ir%50 ==0:
                print(" r bulk indexing... %s, escaped time %s (seconds) "\
                      % ( cnt, tmp - start ) )
            bulk_data = []
            
        

        end = time.time()
        fout.write("Finish  meta-data indexing. Total escaped time %s (seconds) \n"\
                   % (end - start) )
        print("Finish meta-data indexing. Total escaped time %s (seconds) "\
              % (end - start) )
