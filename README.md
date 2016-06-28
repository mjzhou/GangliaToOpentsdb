# GangliaToOpentsdb
collect ganglia metrics store in opentsdb
#System
CentOS6.6
#Config
please edit gmetad ip and opentsdb api in script
```
#gemtad ip
md['gemtadip'] = '172.20.1.51'
#opentsdb api url
md['opentsdb_api'] = 'http://172.20.4.34:4242/api/put?summary''''']'''']
```
#deploy with crontab
*/1 * * * * root python /tmp/ganglia_to_opentsdb.py
