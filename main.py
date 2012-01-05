# -*- coding: utf-8 -*-

import sys
from lib.FileParser import FileParser
from lib.TemplateApplier import TemplateApplier
from lib.FileCreator import FileCreator

from odfpy.odf.opendocument import OpenDocumentText

filelist = sys.argv[1:]


def main(args):
    CREATE_INDIVIDUAL = False
    files = []
    for argument in args:
        if argument in ["-h","--help"]:
           print "Iepaa! Fote't i mira el codi"
           exit()
        elif argument in ["-n","--nojoin"]:
           CREATE_INDIVIDUAL = True
        else:
           files.append(argument)

    if not CREATE_INDIVIDUAL:
       glob = OpenDocumentText()
       dest = files[-1]
       files = files[:-1]
       if files == []:
          print "ERROR: NO INPUT FILES. EXITING..."
          exit()

    c = 0
    for f in files:
        defs = FileParser(f).parse()
        ta = TemplateApplier(defs["TEMPLATE"],defs)
        xml = ta.get()
        addit = False
        if not CREATE_INDIVIDUAL and not c == len(files)-1:
           addit = True
        obj = FileCreator(xml, addit).get()
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
        c += 1
    if not CREATE_INDIVIDUAL:
       glob.save(dest)

main(filelist)
