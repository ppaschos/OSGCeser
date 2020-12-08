#!/usr/bin/env python
from elasticsearch import Elasticsearch, exceptions as es_exceptions
from elasticsearch import helpers
import time
from datetime import datetime
​
​
def get_es_connection():
    """
    establishes es connection.
    """
    print("make sure we are connected to ES...")
    try:
        es_conn = Elasticsearch(
            [{'host': 'atlas-kibana.mwt2.org', 'port': 9200}],
            http_auth=('paschos', 'kemosabe')
        )
        print("connected OK!")
    except es_exceptions.ConnectionError as error:
        print('ConnectionError in get_es_connection: ', error)
    except Exception as e:
        print('Something seriously wrong happened in getting ES connection.', e)
    else:
        return es_conn
​
    time.sleep(70)
​
​
def bulk_index(data, es_conn=None, thread_name=''):
    """
    sends the data to ES for indexing.
    if successful returns True.
    """
    success = False
    if es_conn is None:
        es_conn = get_es_connection()
    try:
        res = helpers.bulk(es_conn, data, raise_on_exception=True, request_timeout=120)
        print(thread_name, "inserted:", res[0], 'errors:', res[1])
        success = True
    except es_exceptions.ConnectionError as error:
        print('ConnectionError ', error)
    except es_exceptions.TransportError as error:
        print('TransportError ', error)
    except helpers.BulkIndexError as error:
        print(error)
    except Exception as e:
        print('Something seriously wrong happened.', e)
​
    return success
​
​
es = get_es_connection()
​
index = 'ligo_benchmarks'
​
data = []
count = 0
​
#for i in range(1):
with open("allsites.log") as f:
	for line in f:
		xx=line.split()
		yy=xx[0:3]
		f1=xx[3]+' '+xx[4]
		dt = datetime.strptime(f1, '%Y-%m-%d %H:%M:%S')
		f1=time.mktime(dt.timetuple())
		f1=int(f1)
		yy=yy+[f1]
		yy=yy+[xx[5]]
		yy=yy+[xx[6]]
		doc = {'_index': index}
		doc['Site'] = yy[0]
		doc['Benchmark']= yy[1]
		doc['Status']= yy[2]
		doc['timestamp']= int(yy[3])
		doc['CPUtime'] = float(yy[4])
		doc['Walltime'] = float(yy[5])
		doc['Efficiency']= float(yy[4])/float(yy[5])
		data.append(doc)
		print(doc)
		if not count % 500:
			print(count)
			res = bulk_index(data, es)
			if res:
				del data[:]
		count += 1
​
​
bulk_index(data, es)
print('final count:', count)
