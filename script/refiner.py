from re import L
import sys, os
import pathlib 
import yaml

class Refiner():

    def __init__(self, ruleFile : pathlib.Path):
        self.rule = yaml.safe_load(open(ruleFile, "r"))["items"]
        # print(self.rule)

    def checkMsg(self, msgName):
        
        msgs = list(filter(None, [item.get("msg") for item in self.rule]))
        for m in msgs:
            if isinstance(m, str):
                if msgName == m:
                    return True
            if isinstance(m, list):
                if msgName in m:
                    return True

        return False

    def checkIE(self, msgName, IEName):

        msgName = msgName.lower()
        IEName = IEName.lower()

        for item in self.rule:

            ie = item.get("ie")
            msg = item.get("msg")
            
            if isinstance(msg, str) or msg == None:
                msgs = [msg]
            elif isinstance(msg, list):
                msgs = msg
            else:
                assert False, ".yaml format error"
            
            for msg in msgs:

                if msg == msgName:
                    if ie == None:
                        return True
                    if isinstance(ie, list):
                        if IEName in ie:
                            return True
                    elif isinstance(ie, str):
                        if IEName == ie:
                            return True
                elif msg == None:
                    if isinstance(ie, list):
                        if IEName in ie:
                            return True
                    elif isinstance(ie, str):
                        if IEName == ie:
                            return True
        
        return False
        
    def getAllInfo(self):

        result = []

        for item in self.rule:
            
            msgs = item.get("msg")
            ies = item.get("ie")
            infos = item.get("info")

            if not infos or not msgs or not ies:
                continue

            msgs = listrize(msgs)
            ies = listrize(ies)
            infos = listrize(infos)

            for msg in msgs:
                for ie in ies:
                    for info in infos:
                        result.append({
                            "msg": msg.lower(),
                            "ie": ie.lower(),
                            "info": info.lower()
                        })

        return result

def listrize(obj):

    if isinstance(obj, list):
        return obj
    else:
        return [obj]

