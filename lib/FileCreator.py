# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup

from odfpy.odf.opendocument import OpenDocumentText
from odfpy.odf.text import P, SoftPageBreak
from odfpy.odf.table import Table, TableColumn, TableRow, TableCell
from odfpy.odf.style import Style, ParagraphProperties, TextProperties, TableColumnProperties
from random import choice

inner = lambda y: "".join([str(x) for x in y.contents])

defaults = {"textalign":"justify","fontweight":"normal","fontsize":"12","fontfamily":"Arial"}

def attr(y,elm):
    try: return inner(elm.find(y))
    except: return defaults[y]

class Doc:
      def __init__(self):
          self.text = []
          self.styles = []

class FileCreator:
      def __init__(self, xml, addlinebreak):
          self.xml = xml
          self.addlinebreak = addlinebreak
          self.handlers = {"text": self._text, "image": self._image, "cols": self._cols}
          self.styles = {}

      def _cols(self, elm, dest):
          width = Style(name="co1", family="table-column")
          width.addElement(TableColumnProperties(columnwidth="2.8cm", breakbefore="auto"))
          self.doc.styles.append(width)
          cols = elm.findAll("column")
          table = Table(name="Columns")
          for c in range(len(cols)): table.addElement(TableColumn(stylename=width, defaultcellstylename="ce1"))

          tr = TableRow()
          table.addElement(tr)
          for col in cols:
              cell = TableCell()
              for elm in col:
                  doc = Doc()
                  doc = self.handlers[elm.name](elm, doc)
                  for a in doc.text: cell.addElement(a)
                  #cell.addElement(#cell.addElement()#P(text=inner(col)))
              tr.addElement(cell)
          dest.text.append(table)
          return dest

      def _text(self, elm, dest):
          s = Style(name=str(choice(range(1000))),family="paragraph")
          s.addElement(TextProperties(fontsize='%spt'%attr("fontsize",elm)))
          s.addElement(TextProperties(fontweight=attr("fontweight",elm)))
          s.addElement(TextProperties(fontfamily=attr("fontfamily",elm)))
          self.doc.styles.append(s)
          paragraphs = inner(elm.find("contents")).split("\n\n")
          for c in paragraphs:
             p = P(text=c,stylename=s)
             dest.text.append(p)
             if len(paragraphs) > 1:
               p = P(text="",stylename=s)
               dest.text.append(p)
          return dest

      def _image(self, elm, dest):
          pass

      def _setStyles(self):
          pass

      def get(self):
          self.doc = Doc()
          b = BeautifulSoup(self.xml)
          for elm in b.page.findAll(["text","image","cols"],recursive=False):
              self.doc = self.handlers[elm.name](elm, self.doc)
          if self.addlinebreak:
             s2 = Style(name="linebreak",family="paragraph")
             s2.addElement(ParagraphProperties(textalign=attr("textalign",elm),breakbefore="page"))
             self.doc.styles.append(s2)
             self.doc.text.append(P(stylename=s2))

          return self.doc
