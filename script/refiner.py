import sys, os
import pathlib 
import yaml

class Refiner():

    def __init__(self, ruleFile : pathlib.Path):
        self.rule = yaml.safe_load(open(ruleFile, "r"))
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
        
        # msgName = msgName.lower()
        # IEName = IEName.lower()

        # if msgName == "attach request":
        #     if IEName in [
        #         "last visited registered tai", 
        #         # "ms network capability",
        #         # "additional update type",
        #         # "security header type",
        #         # "protocol discriminator",
        #         # "mobile station classmark 2",
        #         ]:
        #         return True
        
        # return False #debug

