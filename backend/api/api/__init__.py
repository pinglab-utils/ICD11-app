from flask import Flask, request, jsonify
from flask_cors import CORS

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()
app = Flask(__name__)
CORS(app)

@app.route('/search/disease_search')
def disease_search():
    response = dict()
    queries = request.args.getlist('query')
    if queries:
        query = queries[0]
        print(query)
        response['query'] = query
        s = Search(using=client, index="icd11").query("match", name=query)
        results = s.execute()
        if results:
            response['result'] = results[0].to_dict()
        else:
            response['result'] = dict()
    return jsonify(response)

app.run(host= '0.0.0.0', port=5000)
