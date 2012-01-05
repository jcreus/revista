# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup

from odfpy.odf.opendocument import OpenDocumentText
from odfpy.odf.text import P
from odfpy.odf.style import Style, ParagraphProperties, TextProperties
from random import choice

inner = lambda y: "".join([str(x) for x in y.contents])

defaults = {"textalign":"justify","fontweight":"normal","fontsize":"12","fontfamily":"Arial"}

def attr(y,elm):
    try: return inner(elm.find(y))
    except: return defaults[y]

class FileCreator:
      def __init__(self, fname, xml):
          self.file = fname
          self.xml = xml
          self.handlers = {"text": self._text, "image": self._image}
          self.styles = {}

      def _text(self, elm):
          s = Style(name=str(choice(range(1000))),family="paragraph")
          s.addElement(TextProperties(fontsize='%spt'%attr("fontsize",elm)))
          s.addElement(TextProperties(fontweight=attr("fontweight",elm)))
          s.addElement(TextProperties(fontfamily=attr("fontfamily",elm)))
          s.addElement(ParagraphProperties(textalign=attr("textalign",elm)))
          self.doc.styles.addElement(s)
          paragraphs = inner(elm.find("contents")).split("\n\n")
          for c in paragraphs:
             print c
             p = P(text=c,stylename=s)
             self.doc.text.addElement(p)
             if len(paragraphs) > 1:
               p = P(text="",stylename=s)
               self.doc.text.addElement(p)

      def _image(self, elm):
          pass

      def _setStyles(self):
          pass

      def save(self):
          self.doc = OpenDocumentText()
          self._setStyles()
          b = BeautifulSoup(self.xml)
          for elm in b.page.findAll(["text","image"]):
              self.handlers[elm.name](elm)
          self.doc.save(self.file)
