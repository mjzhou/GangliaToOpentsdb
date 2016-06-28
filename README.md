# GangliaToOpentsdb
collect ganglia metrics store in opentsdb
#System
CentOS6.6
#deploy with crontab
*/1 * * * * root python /tmp/ganglia_to_opentsdb.py
