import os
import warnings

from elasticsearch import Elasticsearch
from opensearchpy import OpenSearch

warnings.filterwarnings("ignore")

logstashHome = "/workspace/logstash/logstash-7.13.2"
configLogstashDir = "/workspace/search_with_machine_learning_course/logstash/config/"
configRawDir = "/workspace/search_with_machine_learning_course/logstash/raw/config/"

elasticsearch = Elasticsearch([{'host': 'localhost', 'port': 9201, 'use_ssl': False}])

opensearchHost = 'localhost'
opensearchPort = 9200
opensearchAuth = ('admin', 'admin')

opensearch = OpenSearch(
    hosts=[{'host': opensearchHost, 'port': opensearchPort}],
    http_compress=True,
    http_auth=opensearchAuth,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


existsQueriesRaw = elasticsearch.indices.exists(index="bbuy_queries_raw")
existsProductsRaw = elasticsearch.indices.exists(index="bbuy_products_raw")

elasticsearch.indices.refresh(index='bb*')
queriesRaw = elasticsearch.count(index="bbuy_queries_raw", ignore_unavailable=True)
productsRaw = elasticsearch.count(index="bbuy_products_raw", ignore_unavailable=True)

queriesRawCount = queriesRaw['count']
productsRawCount = productsRaw['count']

if queriesRawCount == 0 or productsRawCount == 0:
    os.system('kill -9 $(pgrep -f \'logstash\')')

    print(''' - Deleting previous logstash logs''')
    os.system('rm -f /workspace/logs/*')

    print(''' - Building raw indices, please wait, it may take a while!''')
    elasticsearch.indices.delete(index=['bbuy_*'], ignore=[400, 404])

    os.system('nohup {}/bin/logstash --path.settings {} &'.format(logstashHome, configRawDir))

elif queriesRawCount == 1865269 and productsRawCount == 1275077:
    os.system('kill -9 $(pgrep -f \'logstash\')')

    print(''' - Deleting previous logstash logs''')
    os.system('rm -f /workspace/logs/*')

    print(''' - Deleting destination indices''')
    opensearch.indices.delete(index='bb*', ignore=[400, 404])

    print(''' - Running Logstash found in {} '''.format(logstashHome))
    print(''' - Rebuilding destination indices from raw''')
    os.system('nohup {}/bin/logstash --path.settings {} > logstash.log &'.format(logstashHome, configLogstashDir))

else:
    elasticsearch.indices.refresh(index='bb*')
    print(''' 
- Logstash running, PID(s):    
''')
    os.system('pgrep -f \'logstash\'')

    print(''' 
- Still building raw indices, please wait!
    Raw Queries Index: ''' + str(queriesRawCount) + '''/1865269 - ''' + str(
        int((queriesRawCount / 1865269) * 100)) + '''%
    Raw Products Index: ''' + str(productsRawCount) + '''/1275077 - ''' + str(
        int((productsRawCount / 1275077) * 100)) + '''%
''')
