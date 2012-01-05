# -*- coding: utf-8 -*-

import sys
from lib.FileParser import FileParser
from lib.TemplateApplier import TemplateApplier
from lib.FileCreator import FileCreator

from odfpy.odf.opendocument import OpenDocumentText

filelist = sys.argv[1:]

CREATE_INDIVIDUAL = False#True#False

def main(files):
    if not CREATE_INDIVIDUAL:
       glob = OpenDocumentText()
       dest = files[-1]
       files = files[:-1]

    for f in files:
        defs = FileParser(f).parse()
        ta = TemplateApplier(defs["TEMPLATE"],defs)
        xml = ta.get()
        obj = FileCreator(xml).get()
        obj.text = obj.text
        if CREATE_INDIVIDUAL:
           doc = OpenDocumentText()
           for style in obj.styles:
               doc.styles.addElement(style)
           for t in obj.text:
               doc.text.addElement(t)
           doc.save(f+".odt")
        else:
           for style in obj.styles:
               glob.styles.addElement(style)
           for t in obj.text:
               glob.text.addElement(t)
    if not CREATE_INDIVIDUAL:
       glob.save(dest)

main(filelist)
