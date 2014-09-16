>>> escat = elasticsearch.Elasticsearch()
>>> sss = escat.cat.indices()
>>> print sss
health index                pri rep docs.count docs.deleted store.size pri.store.size 
green  logstash-2014.04.16   5   1     852778            0    283.2mb        141.6mb 
green  logstash-2014.04.17   5   1     852515            0    283.2mb        141.5mb 
green  logstash-2014.04.18   5   1     850539            0    282.4mb        141.2mb 
green  logstash-2014.04.19   5   1     851345            0    282.5mb        141.3mb 
green  logstash-2014.04.13   5   1     851578            0    282.6mb        141.3mb 
green  logstash-2014.04.25   5   1     335606            0    218.4mb        109.3mb 
green  logstash-2014.04.12   5   1     852697            0    283.2mb        141.5mb 
green  logstash-2014.04.15   5   1     852843            0    283.3mb        141.6mb 
green  logstash-2014.04.24   5   1     852917            0    283.2mb        141.5mb 
green  logstash-2014.04.23   5   1     852096            0      283mb        141.5mb 
green  logstash-2014.04.14   5   1     852686            0    283.1mb        141.5mb 
green  logstash-2014.04.22   5   1     854081            0    283.8mb        141.8mb 
green  logstash-2014.04.21   5   1     852069            0    282.8mb        141.4mb 
green  logstash-2014.04.20   5   1     851495            0    282.7mb        141.3mb 

>>> for item in tttt:
...     print item.split(" ")
... 
['green', 'logstash-2014.04.16', '5', '1', '852778', '0', '283.2mb', '141.6mb', '']
['green', 'logstash-2014.04.17', '5', '1', '852515', '0', '283.2mb', '141.5mb', '']
['green', 'logstash-2014.04.18', '5', '1', '850539', '0', '282.4mb', '141.2mb', '']
['green', 'logstash-2014.04.19', '5', '1', '851345', '0', '282.5mb', '141.3mb', '']
['green', 'logstash-2014.04.13', '5', '1', '851578', '0', '282.6mb', '141.3mb', '']
['green', 'logstash-2014.04.25', '5', '1', '337417', '0', '', '', '225mb', '112.5mb', '']
['green', 'logstash-2014.04.12', '5', '1', '852697', '0', '283.2mb', '141.5mb', '']
['green', 'logstash-2014.04.15', '5', '1', '852843', '0', '283.3mb', '141.6mb', '']
['green', 'logstash-2014.04.24', '5', '1', '852917', '0', '283.2mb', '141.5mb', '']
['green', 'logstash-2014.04.23', '5', '1', '852096', '0', '', '', '283mb', '141.5mb', '']
['green', 'logstash-2014.04.14', '5', '1', '852686', '0', '283.1mb', '141.5mb', '']
['green', 'logstash-2014.04.22', '5', '1', '854081', '0', '283.8mb', '141.8mb', '']
['green', 'logstash-2014.04.21', '5', '1', '852069', '0', '282.8mb', '141.4mb', '']
['green', 'logstash-2014.04.20', '5', '1', '851495', '0', '282.7mb', '141.3mb', '']
['']




