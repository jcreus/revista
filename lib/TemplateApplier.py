# -*- coding: utf-8 -*-

import re

class TemplateApplier:
  def __init__(self, template, data):
    self.template = template
    self.data = data

  def _specific(self, f):
    if f == "DATE": return "Avui"
    elif f == "IMAGES":
      return ','.join(self.data["LLISTA"])
    raise KeyError

  def _replace(self, res):
    elq = res.group(1).rstrip().lstrip()
    r = None
    r2 = None
    try: r = re.sub("\{(.*?)\}",lambda x: self.data[x.group(1).split("|")[0]] if x.group(1).split("|")[0] in self.data else x.group(1).split("|")[1] ,elq)
    except KeyError:
      print u"Avís: Paràmetre desconegut, no especificat al fitxer de dades"
    try: r2 = re.sub("\[(.*?)\]",lambda x: self._specific(x.group(1)), r or elq)
    except KeyError:
      print u"Avís: Funció desconeguda"
    return r2 or r or elq

  def get(self):
    with open(self.template) as f:
      t = f.read()

    subst = re.sub("<!!(.*?)!!>",self._replace,t)
    return subst
