# -*- coding: utf-8 -*-

import sys
from lib.FileParser import FileParser
from lib.TemplateApplier import TemplateApplier
from lib.FileCreator import FileCreator

filelist = sys.argv[1:]

def main(files):
    for f in files:
        defs = FileParser(f).parse()
        ta = TemplateApplier(defs["TEMPLATE"],defs)
        xml = ta.get()
        FileCreator(f+".odt",xml).save()

main(filelist)
