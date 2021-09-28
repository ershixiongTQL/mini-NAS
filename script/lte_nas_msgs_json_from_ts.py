# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Inches
import re, os, sys
import json

MSG_BODY_TB_HDR = [
    "iei",
    "information element",
    "type/reference",
    "presence",
    "format",
    "length",
]

IE_FORMATS = [
    "T","V","TV","LV","TLV","LV-E","TLV-E" #TS 24.007
]

def getTableFirstRow(tb):
    firstRow = tb[0]
    cellsText = []
    for cell in firstRow:
        cellsText.append(cell.strip())
    return cellsText

def getDocxTableFirstRow(tb):
    firstRow = tb.rows[0]
    cells = firstRow.cells
    cellsText = []
    
    for i in range(len(cells)):
        if i != 0 and cells[i-1] is cells[i]:
            continue
        cell = cells[i]
        if cell is None:
            continue
        cellsText.append(cell.text.strip())

    return cellsText

def docxTbSimplify(tb):
    simplified = []

    for row in tb.rows:
        cells = row.cells
        cellsText = []

        for i in range(len(cells)):
            
            if cells[i] is None:
                continue
            if i != 0 and cells[i-1] is cells[i]:
                continue

            cellText = cells[i].text.strip()
            cellText = re.sub(r"[\n\r]", " ", cellText)
            cellText = re.sub(r"\s+", " ", cellText)
            cellsText.append(cellText)

        simplified.append(cellsText)

    return simplified

def tbToText(tb):
    
    rowsList = tableListAlign(tb)
    
    text = ""
    for row in rowsList:
        text += " | ".join(row) + "\n"
    
    return text

def tableListAlign(tbli):

    aligns = []

    maxRowLen = 0
    for row in tbli:
        if len(row) > maxRowLen:
            maxRowLen = len(row)
    
    for i in range(maxRowLen):
        align = 0
        for row in tbli:
            if len(row) <= i:
                break
            
            cellLen = len(row[i])
            if cellLen > align:
                align = cellLen
            
        aligns.append(align)

    for i,row in enumerate(tbli):
        for j,cell in enumerate(row):
            tbli[i][j] = cell.ljust(aligns[j])
    
    return tbli

def formatClean(string):
    string = re.sub(r"[\r\n]", " ", string)
    string = re.sub(r"\s+", " ", string)
    return string.strip()

class MSGBody():

    def __init__(self, tb):
        
        self._msgType = ""
        self.tb = tb
        self._hdr = tb[0]

        self._IEs = []
        
        for ie in tb[1:]:
            IE = {}
            
            for i in range(len(self._hdr)):
                
                key = formatClean(self._hdr[i]).lower()
                attr = formatClean(ie[i])
                
                if key == "type/reference":
                    attr = re.sub(r"\s+(?:9[0-9]*)?\..*$", "", attr).strip()
                    key = "type"
                
                if key == "information element":
                    key = "ie"
                IE[key] = attr

                if key == "type":
                    if "message type" in attr.lower():
                        msgType = formatClean(IE["ie"]).lower()
                        msgType = re.sub(r"\s+((message identity)|(message type)|(message))\s*$", "", msgType)
                        self._msgType = msgType.strip()

            self._IEs.append(IE)

    @property
    def IEs(self):
        return self._IEs
    
    @property
    def IEProperties(self):
        return self._hdr

    @property
    def MsgType(self):
        return self._msgType

    def __str__(self):
        string = "message [" + self._msgType + "]\n"
        string += tbToText(self.tb)
        return string

def main(doc):

    tbs = doc.tables
    msgBodies = []
    comb = {}

    for i, tb in enumerate(tbs):
        
        hdr = getDocxTableFirstRow(tb)
        for i in range(len(hdr)):
            hdr[i] = hdr[i].lower()

        if hdr == MSG_BODY_TB_HDR:
            msgBodies.append(MSGBody(docxTbSimplify(tb)))

    for msbb in msgBodies:
        if not msbb.MsgType:
            print("msg no type: %s" %(msbb))
            continue
        # else:
        #     print(msbb)
        comb[msbb.MsgType.lower()] = msbb.IEs
    
    f = open("./lte_nas_msgs.json", mode = "w+")
    json.dump(comb, fp=f)
    f.close()

if __name__ == "__main__":

    if len(sys.argv) < 2:
        exit("expect 3GPP 24.301(NAS) TS .docx file")
    
    tsFile = sys.argv[1]
    
    doc = Document(tsFile)

    main(doc)

