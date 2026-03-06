import requests
class HttpRequest:
    def __init__(self):
        self.session = requests.Session()
    def send(self,method,url,headers=None,params=None,json=None):
        try:
            method = method.lower()
            if method == "get":
                return self.session.get(url,headers=headers,params=params,timeout=10)
            elif method == "post":
                return self.session.post(url,headers=headers,json=json,timeout=10)
            else:
                return None
        except Exception as e:
            logger.error(f"请求异常{e}")
            return None
