import vk_api
import json


class VKApi():
    def __init__(self,authToken):
        self.vk_session = vk_api.VkApi(token=authToken)
        pass
    
    def getDialog(self,user):
        pass

    def userInfo(self,user):
        pass
    
    def sendMessage(self,message):
        pass