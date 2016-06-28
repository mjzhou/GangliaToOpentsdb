#!/usr/bin/env python
import sys
import socket
import xml.parsers.expat
import urllib2
import time
md = {}
#gemtad ip
md['gemtadip'] = '172.20.1.51'
#opentsdb api url
md['opentsdb_api'] = 'http://172.20.4.34:4242/api/put?summary'
#metric map
md['bytes_in'] = 'system.net.in'
md['bytes_out'] = 'system.net.out'
md['bytes_sum'] = 'system.net.sum'
md['cpu_idle'] = 'system.cpu.idle'
md['cpu_num'] = 'system.cpu.num'
md['cpu_system'] = 'system.cpu.system'
md['cpu_user'] = 'system.cpu.user'
md['cpu_wio'] = 'system.cpu.wio'
md['ib_in'] = 'system.ib.in'
md['ib_out'] = 'system.ib.out'
md['ib_sum'] = 'system.ib.sum'
md['io_nread'] = 'system.io.nread'
md['io_nrwtot'] = 'system.io.nrwtot'
md['io_nwrite'] = 'system.io.nwrite'
md['load_fifteen'] = 'system.load.15'
md['load_five'] = 'system.load.5'
md['load_one'] = 'system.load.1'
md['mem_buffers'] = 'system.mem.buffers'
md['mem_cached'] = 'system.mem.cached'
md['mem_free'] = 'system.mem.free'
md['mem_shared'] = 'system.mem.shared'
md['mem_total'] = 'system.mem.total'
md['proc_run'] = 'system.proc.run'
md['proc_total'] = 'system.proc.total'
class GParser:
  def __init__(self):
    self.inhost =0
    self.inmetric = 0
    self.value = None
    self.group = None
    self.host = None
    self.now = None
    self.url = md['opentsdb_api']
    self.ghost = self.ganglia_host()
    self.json = ''

  def parse(self, file):
    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = self.start_element
    p.EndElementHandler = self.end_element
    p.ParseFile(file)

  def start_element(self, name, attrs):
    if name == "CLUSTER":
        self.group = attrs["NAME"]
    elif name == "HOST":
      self.host = attrs["NAME"]
      self.now = attrs["REPORTED"]
      #self.now = int(time.time())
      self.inhost=1
    elif self.inhost==1 and name == "METRIC":
      try:
        #filter string type metrics
        value = '%.2f' % float(attrs["VAL"])
        if 'system_' not in str(attrs["NAME"]):
          #print attrs["NAME"],d[attrs["NAME"]]
          data = '{"metric":"'+str(md[attrs["NAME"]])+'","timestamp":'+str(self.now)+', "value":'+str(value)+', "tags":{"host":"'+self.host+'", "group":"'+self.group+'"}},'
          self.json += data
      except BaseException , e:
        pass
  def end_element(self, name):
    if name == "HOST" and self.inhost==1:
      self.send(self.json)
      self.json=''
      self.inhost=0

  def send(self,data):
    if(data[:-1]):
      content = '['+data[:-1]+']'
      #print content
      try:
          f = urllib2.urlopen(self.url,content)
          #print f.read()
      except BaseException , e:
        pass
  #if you read data from group gmond header
  def gmond_host(self):
    ip = None
    gmondConf = '/etc/ganglia/gmond.conf'
    with open(gmondConf,'r') as gf:
      for line in gf:
        if 'host =' in line:
          ip = line.split('=')[1][1:-1]
          break
    return ip
  def run(self):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      #gmetad server or gmond_host,recommand set gmetad server ip
      s.connect((md['gemtadip'],8651))  
      sfile = s.makefile("r")
      s.close()
      flag = self.parse(sfile)
      sfile = None
    except BaseException , e:
      #pass
      print e
if __name__='__main__':
    GParser().run()
#while True:
#  GParser().run()
#  time.sleep(30)
