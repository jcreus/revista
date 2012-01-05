# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re
from BeautifulSoup import BeautifulSoup

inner = lambda y: "".join([unicode(x) for x in y.contents]) 

class FileParser:
  def __init__(self, url):
    self.url = url

  def parse(self):
    with open(self.url) as f:
      t = unicode(f.read(),"utf-8")
    defs = {}
    parse = BeautifulSoup(t)
    defs["TEMPLATE"] = inner(parse.find("template"))
    for elm in parse.file:
        if "name" in dir(elm):
           tag = elm.name
           if tag != "template":
              defs[tag] = inner(elm)
    print defs
    return defs
