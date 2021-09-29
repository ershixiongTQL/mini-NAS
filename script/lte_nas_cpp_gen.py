# -*- coding: UTF-8 -*-

import os, sys, re, json, argparse
from typing import List, Optional
import pathlib
from NASConstants import EMM_TYPES, ESM_TYPES
from refiner import Refiner

argParser = argparse.ArgumentParser()
argParser.add_argument("nas_msg_def", type = open)
argParser.add_argument("refine_rule", type = pathlib.Path, help=".yaml file used to refine the output")
argParser.add_argument("--ie_modules", type = pathlib.Path, help="dir which contains code supports specific IE")
argParser.add_argument("--target_dir", type = pathlib.Path, default="gen", help="destdir to hold the generated codes")

args = argParser.parse_args()

IE_MODULES = None

def loadMessageDefenition():
    msgDef = args.nas_msg_def.read()
    return json.loads(msgDef)

def getMessageTypeId(msg):
    msgTypeId = EMM_TYPES.get(msg)
    if msgTypeId is None:
        msgTypeId = ESM_TYPES.get(msg)
    if msgTypeId is None:
        print("Message Type ID of \"%s\" notfound" %(msg))
        return None

    return msgTypeId

def targetDirPrepare():
    target = args.target_dir
    
    if os.path.isdir(target):
        # exit("target dir %s already exist" %(target))
        return target

    if not os.mkdir(target):
        exit("failes to create target dir %s" %(target))

    return target

def nameFormat(src):
    src = re.sub(r"[\n\r]", " ", src)
    src = re.sub(r"(\s+)|-|'", "_", src)
    return src.lower().strip()

class IEModules():

    def __init__(self, dirs : pathlib.Path):
        
        self.ieSupports = []
        self.infoSwitches = {}
        
        for root, dirs, files in os.walk(dirs):
            for file in files:
                found = re.search(r"^nas_ie_(.*)(?:\.c|\.cpp)$", file)
                if found:
                    self.ieSupports.append(found.group(1).replace("_", " "))

    def getModuleHdr(self, name):
        # hdrs = [hdr for hdr in self.ieSupports if hdr.withprefix("nas_ie_%s" %(nameFormat(name).lower()))]
        # return hdrs[0]
        return "nas_ie_%s.h" %(nameFormat(name).lower())

    def infoSwitchOn(self, ie_type, info_name):
        
        if ie_type in self.infoSwitches:
            if info_name not in self.infoSwitches[ie_type]:
                self.infoSwitches[ie_type].append(info_name)
        else:
            self.infoSwitches[ie_type] = [info_name]

    def getInfoSwitches(self, ie_type):
        if ie_type not in self.infoSwitches:
            return []
        return self.infoSwitches[ie_type]

    def getAllInfoSwitches(self):
        switches = []
        for ie in self.ieSupports:
            if ie in self.infoSwitches:
                switches += self.infoSwitches[ie]
        return switches

    @property
    def modules(self):
        return self.ieSupports

    def __len__(self):
        return len(self.ieSupports)

    def __str__(self):
        return "Support IEs:\n" + str(self.ieSupports)

class cppCode():

    def __init__(self, fileName):
        self._name = nameFormat(fileName)
        
        self._incs = []
        self._enums = {}
        self._funcs = []
        self._funcsContent = {}
        self._macroVal = []
    
    def addInclude(self, include):
        if include != None:
            self._incs.append(include)
    
    def addMacroVal(self, name, val, static = True):
        self._macroVal.append({
            "name":name,
            "val":val,
            "static":static,
        })
    
    def addFunction(self, type, funcName, params, static = True, inline = False):
        self._funcs.append({
            "type":type,
            "name":funcName,
            "params":params,
            "static":static,
            "inline":inline,
        })
    
    def addEnum(self, enumName, enums, public = False):
        self._enums[enumName] = {"name": enumName, "items" : enums, "public": public}

    def fillFunction(self, funcName, code):
        code = re.sub(r"^", "\t", code, flags=re.MULTILINE) + "\n"
        self._funcsContent[funcName] = code
    
    def dumps(self, targetPath: pathlib.Path):
        
        #.c/.cpp
        code = ""
        code += self._includesDump() + "\n"
        code += self._macroValDump(False) + "\n"
        code += self._enumDump(False) + "\n"
        code += self._funcDeclarationDump() + "\n"
        code += self._funcDump() + "\n"
        
        code = code.replace("$NAME$", self._name.upper()).replace("$name$", self._name)

        fp = open(os.path.join(targetPath, self._name + ".c"), mode="w+")
        assert fp != None
        fp.write(code)
        fp.close

        #.h/.hh
        code = ""
        code += "#ifndef _%s_H_" %(self._name.upper()) + "\n"
        code += "#define _%s_H_" %(self._name.upper()) + "\n\n"
        code += self._includesDump() + "\n"
        code += self._macroValDump(True) + "\n"
        code += self._enumDump(True) + "\n"
        code += self._funcDeclarationDump(False) + "\n"
        code += "\n#endif" + "\n"

        code = code.replace("$NAME$", self._name.upper()).replace("$name$", self._name)

        fp = open(os.path.join(targetPath, self._name + ".h"), mode="w+")
        assert fp != None
        fp.write(code)
        fp.close

    def _includesDump(self):
        code = ""
        for inc in self._incs:
            if self._name + ".h" == inc:
                continue
            code += "#include \"%s\"" %(nameFormat(inc)) + "\n"
        return code

    def _macroValDump(self, public):

        code = ""

        static = not public
        ms = [ms for ms in self._macroVal if ms["static"] == static]
        if not ms:
            return ""
        for m in ms:
            code += "#define %s %s" %(m["name"], m["val"])
            if isinstance(m["val"], int):
                code += " //0x%x" %(m["val"])
            code += "\n"
        
        return code
        
    def _enumDump(self, public):

        blocks = []

        enums = [self._enums[e] for e in self._enums if self._enums[e]["public"] == public]

        for enum in enums:
            block = []
            block.append("typedef enum %s_e{" %(enum["name"]))
            for item in enum["items"]:
                block.append("\t%s," %(nameFormat(item).upper()))
            block.append("}%s_t;" %(enum["name"]))
            block.append("")
            blocks += block
        
        return "\n".join(blocks)

    def getFunctions(self, static = None):
        return [func for func in self._funcs if static is None or func["static"] == static]

    def _funcDeclarationDump(self, static = True):
        code = ""

        funcs = self.getFunctions(static = static)
        
        for func in funcs:
            if static:
                code += "static "
            code += "%s %s(%s);\n" %(func["type"], func["name"], ", ".join(func["params"]))
        
        return code
    
    def _funcDump(self):

        funcBlocks = []

        funcs = self.getFunctions()

        for func in funcs:
            code = ""
            if func["static"]:
                code += "static "
            if func["inline"]:
                code += "inline "
            code += "%s %s(%s){\n" %(func["type"], func["name"], ", ".join(func["params"]))
            
            content = self._funcsContent.get(func["name"])
            if content is not None:
                code += content
            
            code += "}\n"
            funcBlocks.append(code)
        
        return "\n".join(funcBlocks)
        
class NASMessageParseCode(cppCode):

    def __init__(self, msgName, msgDef):

        fileName = "nas_msg_" + msgName
        super(NASMessageParseCode, self).__init__(fileName)

        self.msgDef = msgDef
        self.msgName = msgName
        
        self.optionalIEs = [ie for ie in self.msgDef if ie["presence"].upper() != "M"]
        self.mandatoryIEs = [ie for ie in self.msgDef if ie["presence"].upper() == "M"]
        
        self.fullIEIs = [ie for ie in self.optionalIEs if "-" not in ie["iei"]]
        self.halfIEIs = [ie for ie in self.optionalIEs if "-" in ie["iei"]]

        self.aimOptIEs = [ie for ie in self.optionalIEs if REFINER.checkIE(self.msgName, ie["ie"])]
        self.aimOptFullIEIs = [ie for ie in self.aimOptIEs if "-" not in ie["iei"]]
        self.aimOptHalfIEIs = [ie for ie in self.aimOptIEs if "-" in ie["iei"]]

        self.aimMandaIEs = [ie for ie in self.mandatoryIEs if REFINER.checkIE(self.msgName, ie["ie"])]
        self.aimMandaFullIEIs = [ie for ie in self.aimMandaIEs if "-" not in ie["iei"]]
        self.aimMandaHalfIEIs = [ie for ie in self.aimMandaIEs if "-" in ie["iei"]]

        self.addInclude("lte_nas_ie.h")
        self.addInclude(fileName + ".h")
        for ie in [ie for ie in self.msgDef if REFINER.checkIE(self.msgName, ie["ie"])]:
            self.addInclude(IE_MODULES.getModuleHdr(ie["type"]))

        self.addEnum("$name$_content", [self.msgName + "_" + ie["ie"] for ie in msgDef], public=True)

        # self.addFunction("void", "ie_info_noticer", ["unsigned int info_id", "unsigned char *info", "unsigned short len", "void *priv"])
        self.addFunction("unsigned short", "mandatory_ies_parse", ["unsigned char *data", "unsigned short len", "struct nas_msg_noticer_priv *priv"])
        self.addFunction("void", "$name$_parse", ["unsigned char *data", "unsigned short len", "struct nas_msg_noticer_priv *priv"], static = False)
        self.addFunction("const char *", "$name$_ie_id_to_str", ["unsigned int ie"], static = False)
        self.addFunction("const char *", "$name$_ie_info_id_to_str", ["unsigned int ie", "unsigned int info"], static = False)

        # self.ieNoticerFuncFill()
        self.mandatoryIesParseFuncFill()
        self.parseFuncFill()
        self.msgIEToNameFuncFill()
        self.msgIEInfoToNameFuncFill()
    
    def ieNoticerFuncFill(self):
        lines = []
        lines.append("struct nas_msg_noticer_priv *private = (struct nas_msg_noticer_priv *)priv;")
        lines.append("private->noticer(private->msg_id, private->msg_ie_id, info_id, info, len);")
        self.fillFunction("ie_info_noticer", "\n".join(lines))

    def mandatoryIesParseFuncFill(self):
        lines = []
        mandatories = [ie for ie in self.msgDef if ie["presence"].upper() == "M"]

        if not mandatories:
            self.fillFunction("ie_info_noticer", "return 0;")
            return

        lines.append("unsigned char *data_orig = data;")
        lines.append("")

        halfByteInd = False
        for ie in mandatories:

            valLength = lteNasIEValueLenResolve(ie)
            valueOffset = lteNasIEValueOffset(ie)
            
            if ie["length"] == "1/2":
                halfByteInd = not halfByteInd
                valLength = "0" if halfByteInd else "1"

            if REFINER.checkIE(self.msgName, ie["ie"]):
                lines.append("priv->msg_ie_id = %s;" %(nameFormat(self.msgName + "_" + ie["ie"]).upper()))
                if ie["length"] == "1/2":
                    lines.append("nas_ie_%s_parse(data + %s, %d, ie_info_noticer, (void *)priv);" %(nameFormat(ie["type"]), valueOffset, 0 if halfByteInd else 1))
                else:
                    lines.append("nas_ie_%s_parse(data + %s, %s, ie_info_noticer, (void *)priv);" %(nameFormat(ie["type"]), valueOffset, valLength))
            
            lines.append("data += (%s + %s); /*skip IE %s(%s)*/" %(valueOffset, valLength, ie["ie"], ie["type"]))

        lines.append("return data - data_orig;")

        self.fillFunction("mandatory_ies_parse", "\n".join(lines))

    def parseFuncFill(self):

        lines = []

        lines.append("lte_nas_ie_parser _parser;")
        lines.append("unsigned short parsed_len = 0;")
        lines.append("unsigned char target_ies_left = %d; //IEs assigned" %(len(self.aimOptIEs)))
        lines.append("")
        lines.append("parsed_len += mandatory_ies_parse(data, len, priv);")
        
        lines.append("")
        lines.append("while(target_ies_left && (len > parsed_len)){")

        lines.append("\tunsigned int ie_val_len;")
        lines.append("\tunsigned char msg_value_offset = 1; //default")
        lines.append("\tunsigned char *ie_pos = data + parsed_len;")
        lines.append("")

        lines.append("\tswitch(IEI(ie_pos)){")
        fmtCates = {}
        for ie in self.fullIEIs:
            if not fmtCates.get(ie["format"]):
                fmtCates[ie["format"]] = [ie]
            else:
                fmtCates[ie["format"]].append(ie)
        for cate in fmtCates:
            lines.append("\t\t/*IE format: %s*/" %(fmtCates[cate][0]["format"]))
            cateFmt = fmtCates[cate][0]["format"]
            if "l" in cateFmt.lower():
                lines.append("\t\t" + " ".join(["case 0x%s:" %(ie["iei"].strip("-")) for ie in fmtCates[cate]]))
                lines.append("\t\t\tie_val_len = %s;" %(lteNasIEValueLenResolve(fmtCates[cate][0], "ie_pos")))
                lines.append("\t\t\tmsg_value_offset = %d;" %(lteNasIEValueOffset(fmtCates[cate][0])))
                lines.append("\t\t\tbreak;")
            else:
                for ie in fmtCates[cate]:
                    lines.append("\t\tcase 0x%s: ie_val_len = %s; break;" %(ie["iei"].strip("-"), lteNasIEValueLenResolve(ie, "ie_pos")))
                
        lines.append("\t\tdefault:")

        if self.halfIEIs:
            lines.append("\t\t\tswitch(IEI(ie_pos) & 0xf0){")
            lines.append("\t\t\t\t" + " ".join(["case 0x%s:" %(ie["iei"].strip("-")) for ie in self.halfIEIs]))
            lines.append("\t\t\t\t\tie_val_len = 1;")
            lines.append("\t\t\t\t\tmsg_value_offset = 0; break;")
            lines.append("\t\t\t\tdefault: return; //unknown IEI")
            lines.append("\t\t\t}")
        else:
            lines.append("\t\t\treturn;")
        lines.append("\t}")
        lines.append("")

        lines.append("\tswitch(IEI(ie_pos)){")

        for ie in self.aimOptFullIEIs:
            lines.append("\t\tcase 0x%s:" %(ie["iei"].replace("-", "")))
            lines.append("\t\t\t/*%s(%s) fmt %s length %s*/" %(ie["ie"], ie["type"], ie["format"], ie["length"]))
            lines.append("\t\t\tpriv->msg_ie_id = %s;" %(nameFormat(self.msgName + "_" + ie["ie"]).upper()))
            lines.append("\t\t\t_parser = nas_ie_%s_parse; break;" %(nameFormat(ie["type"])))
        
        lines.append("\t\tdefault: ")

        if self.aimOptHalfIEIs:
            lines.append("\t\t\tswitch(IEI(ie_pos) & 0xf0){")
            for ie in self.aimOptHalfIEIs:
                lines.append("\t\t\t\tcase 0x%s: " %(ie["iei"].replace("-", "")))
                lines.append("\t\t\t\t\t/*%s(%s) fmt %s length %s*/" %(ie["ie"], ie["type"], ie["format"], ie["length"]))
                lines.append("\t\t\t\t\tpriv->msg_ie_id = %s;" %(nameFormat(self.msgName + "_" + ie["ie"]).upper()))
                lines.append("\t\t\t\t\t_parser = nas_ie_%s_parse; break;" %(nameFormat(ie["type"])))
            lines.append("\t\t\t\tdefault: goto SKIP_PARSE;")
            lines.append("\t\t\t}")
        else:
            lines.append("\t\t\tgoto SKIP_PARSE;")
        
        lines.append("\t}")
        lines.append("")

        lines.append("\t_parser(ie_pos + msg_value_offset, ie_val_len, ie_info_noticer, (void *)priv);")
        lines.append("\ttarget_ies_left--;")

        lines.append("")
        lines.append("\tSKIP_PARSE:")
        lines.append("\tparsed_len += msg_value_offset + ie_val_len;")

        lines.append("}")
        self.fillFunction("$name$_parse", "\n".join(lines))

    def msgIEToNameFuncFill(self):

        lines = []

        lines.append("switch(ie){")
        for ie in self.msgDef:
            lines.append("\tcase %s: return \"%s\";" %(nameFormat(self.msgName + "_" + ie["ie"]).upper(), ie["ie"]))
        lines.append("\tdefault: return \"unknown IE\";")
        lines.append("}")
        self.fillFunction("$name$_ie_id_to_str", "\n".join(lines))

    def msgIEInfoToNameFuncFill(self):

        lines = []

        lines.append("switch(ie){")
        for ie in self.aimOptIEs + self.aimMandaIEs:
            funcName = "nas_ie_%s_info_id_to_str" %(nameFormat(ie["type"]))
            ieEnumName = nameFormat(self.msgName + "_" + ie["ie"]).upper()
            if IEModuleExam(ie["type"], funcName + r"\s*\("):
                lines.append("\tcase %s: " %(ieEnumName))
                lines.append("\t\treturn %s(info);" %(funcName))
            else:
                lines.append("\tcase %s: return \"?\";" %(ieEnumName))
        lines.append("\tdefault: return \"?\";")
        lines.append("}")
        self.fillFunction("$name$_ie_info_id_to_str", "\n".join(lines))

class NASMessageCode(cppCode):

    NAME = "nas_msg_parser"

    def __init__(self, msgDefs):
        super(NASMessageCode, self).__init__(self.NAME)

        self.msgs = msgDefs
        self.interestedMsgs = {}

        for msg in msgDefs:
            if REFINER.checkMsg(msg):
                self.interestedMsgs[msg] = msgDefs[msg]

        self.addInclude("lte_nas_ie.h")
        self.addInclude(self.NAME + ".h")

        for msg in self.interestedMsgs:
            self.addInclude("nas_msg_%s.h" %(msg))
            if msg in EMM_TYPES:
                self.addMacroVal("MSG_" + nameFormat(msg).upper(), EMM_TYPES[msg])
            if msg in ESM_TYPES:
                self.addMacroVal("MSG_" + nameFormat(msg).upper(), ESM_TYPES[msg])

        self.addFunction("const char *", "nas_msg_type_to_str", ["unsigned int msg_type"], static=False)
        self.addFunction("const char *", "nas_msg_ie_id_to_str", ["unsigned int msg_type", "unsigned int msg_ie_id"], static=False)
        self.addFunction("const char *", "nas_msg_ie_info_id_to_str", ["unsigned int msg_type", "unsigned int msg_ie_id", "unsigned int ie_info_id"], static=False)
        self.addFunction("void", "nas_msg_parse", ["unsigned char *data", "unsigned short len", "lte_nas_msg_noticer cb"], static=False)
    
        self.nasMsgTypeToStrFuncFill()
        self.nasMsgIEIDToStrFuncFill()
        self.nasMsgIEInfoIDToStrFuncFill()
        self.nasMsgParseFuncFill()
    
    def nasMsgTypeToStrFuncFill(self):
        lines = []

        lines.append("switch(msg_type){")
        for msg in self.interestedMsgs:
            lines.append("\tcase MSG_%s: return \"%s\";" %(nameFormat(msg).upper(), msg))
        lines.append("\tdefault: return \"?\";")
        lines.append("}")

        self.fillFunction("nas_msg_type_to_str", "\n".join(lines))
    
    def nasMsgIEIDToStrFuncFill(self):
        lines = []

        lines.append("switch(msg_type){")
        for msg in self.interestedMsgs:
            lines.append("\tcase MSG_%s: return nas_msg_%s_ie_id_to_str(msg_ie_id);" %(nameFormat(msg).upper(), nameFormat(msg)))
        lines.append("\tdefault: return \"?\";")
        lines.append("}")

        self.fillFunction("nas_msg_ie_id_to_str", "\n".join(lines))
    
    def nasMsgIEInfoIDToStrFuncFill(self):
        lines = []

        lines.append("switch(msg_type){")
        for msg in self.interestedMsgs:
            lines.append("\tcase MSG_%s: return nas_msg_%s_ie_info_id_to_str(msg_ie_id, ie_info_id);" %(nameFormat(msg).upper(), nameFormat(msg)))
        lines.append("\tdefault: return \"?\";")
        lines.append("}")

        self.fillFunction("nas_msg_ie_info_id_to_str", "\n".join(lines))
    
    def nasMsgParseFuncFill(self):

        lines = []

        lines.append("struct nas_msg_noticer_priv priv;")
        lines.append("")

        lines.append("if (len < 2 || *data != 0x07) return;")

        lines.append("priv.noticer = cb;")
        lines.append("priv.msg_id = data[1];")
        lines.append("")

        lines.append("switch(priv.msg_id){")

        for msg in self.interestedMsgs:
            N = nameFormat(msg)
            lines.append("\tcase MSG_%s: nas_msg_%s_parse(data, len, &priv); break;" %(N.upper(), N))
        lines.append("\tdefault: break;")
        lines.append("}")

        self.fillFunction("nas_msg_parse", "\n".join(lines))

def IEModuleExam(moduleName, pattern):
    
    filePath = os.path.join(args.ie_modules, "nas_ie_%s.c" %(nameFormat(moduleName)))
    if not os.path.exists(filePath):
        return False
    
    file = open(filePath, "r")
    if not file:
        return False
    
    content = file.read()

    found = re.search(pattern, content)
    
    return True if found else False

def lteNasIEValueLenResolve(ie: dict, dataName = "data"):

    code = "[???]"
    fmt = ie["format"].lower().strip()
    ext = False
    if "-e" in fmt:
        ext = True
        fmt = fmt.replace("-e", "")

    fmtStruct = "struct ie_hdr_%s" %(fmt)
    
    if fmt == "v":
        code = ie["length"]
    elif fmt == "tv":
        code = str(int(ie["length"]) - 1)
    elif fmt in ["tlv", "lv"]:
    
        if ext:
            fmtStruct += "_e"
            code = "ntohs(((%s *)%s)->l)" %(fmtStruct, dataName)
        else:
            code = "((%s *)%s)->l" %(fmtStruct, dataName)
    else:
        print("unknown format %s" %(ie["format"]))
    
    return code

def lteNasIEValueOffset(ie: dict):

    fmt = ie["format"].lower().strip()
    ext = False
    if "-e" in fmt:
        ext = True
        fmt = fmt.replace("-e", "")
    
    if fmt == "v":
        return 0
    elif fmt == "tv":
        return 1
    elif fmt == "tlv":
        return 3 if ext else 2
    elif fmt == "lv":
        return 2 if ext else 1
    else:
        print("unknown format %s" %(ie["format"]))

def nasIEInfoSwitchAssign(msgDefs):

    allCares = REFINER.getAllInfo()

    for msg_name in msgDefs:
        msg = msgDefs[msg_name]
        for ie in msg:
            ie_name = ie["ie"].lower()
            ie_type = ie["type"].lower()

            cares = [care for care in allCares if care["msg"] == msg_name.lower() and care["ie"] == ie_name]

            for care in cares:
                IE_MODULES.infoSwitchOn(ie_type, care["info"])

def dumpIEInfoEnableFiles(targetPath):

    modules = IE_MODULES.modules

    for module in modules:
        file = open(os.path.join(targetPath, "nas_ie_%s_info_enable.h" %(nameFormat(module))), "w")

        infosEn = IE_MODULES.getInfoSwitches(module)

        code = ""

        code += "#ifndef _NAS_IE_%s_INFO_ENABLE_H_" %(nameFormat(module).upper())+ "\n"
        code += "#define _NAS_IE_%s_INFO_ENABLE_H_" %(nameFormat(module).upper())+ "\n\n"
        
        code += "//%d INFO(s) SWITCHED ON" %(len(infosEn)) + "\n"

        for info in infosEn:
            code += "#define CARE_%s_%s" %(nameFormat(module).upper(), nameFormat(info).upper()) + "\n"
        
        code += "\n#endif" + "\n"
        
        file.write(code)

        file.close()
    
def main():

    msgDefs = loadMessageDefenition()
    targetPath = targetDirPrepare()
    
    allIETypes = []
    for ies in [ msgDefs[msg] for msg in msgDefs ]:
        allIETypes += ies
    
    IETypesDict = {}
    for ie in allIETypes:

        ieType = ie["type"]
        
        if "-" in ie["iei"]:
            if ie["format"] != "TV":
                print("bad IE:", str(ie))
        
        IETypesDict[ieType] = ie
    
    for msg in msgDefs:
        if REFINER.checkMsg(msg):
            NASMessageParseCode(msg, msgDefs[msg]).dumps(targetPath)

    NASMessageCode(msgDefs).dumps(targetPath)

    nasIEInfoSwitchAssign(msgDefs)

    dumpIEInfoEnableFiles(targetPath)

REFINER = Refiner(args.refine_rule)
IE_MODULES = IEModules(args.ie_modules)

main()
