import requests, json
from dataclasses import dataclass

def append_to_url(base_url,param):
    return "%s%s/" % (base_url,param)

@dataclass
class Response():
    request_url: str
    status_code: int
    json_data: dict

    def __str__(self) -> str:
        str = "data from url: {url} \n status:{status}\n data: \n {data}"
        return str.format(
            url = self.request_url,
            status = self.status_code,
            data = self.json_data
            )

    def __getitem__(self,key):
        return self.json_data[key]
    
class RestConsumer(object):

    def __init__(self,base_url):
        self.base_url = base_url if base_url[-1] == '/' else "%s%s" % (base_url,"/")

    def set_base_url(self, base_url):
        self.base_url = base_url if base_url[-1] == '/' else "%s%s" % (base_url,"/")

    def get_base_url(self):
        return self.base_url

    def __getattr__(self,key):
        new_base = append_to_url(self.base_url,key)
        return self.__class__(base_url=new_base)
    
    def __getitem__(self,key):
        return self.__getattr__(key)

    def __call__(self, **kwargs):
        print ("Calling %s" % self.base_url)
        return self.get(self.base_url,**kwargs)

    def get(self,url,**kwargs):
        r = requests.get(url,**kwargs)
        return Response(
            self.base_url, 
            r.status_code, 
            json.loads(r.content)
        )

    def post(self,**kwargs):
        r = requests.post(self.base_url, **kwargs)
        return Response(
            self.base_url, 
            r.status_code, 
            json.loads(r.content)
        )

    def put(self,**kwargs):
        r = requests.put(self.base_url, **kwargs)
        return Response(
            self.base_url, 
            r.status_code, 
            json.loads(r.content)
        )
    
    def patch(self, **kwargs):
        r = requests.patch(self.base_url, **kwargs)
        return Response(
            self.base_url, 
            r.status_code, 
            json.loads(r.content)
        )
    
    def delete(self, **kwargs):
        r = requests.delete(self.base_url, **kwargs)
        return Response(
            self.base_url, 
            r.status_code, 
            json.loads(r.content)
        )


if __name__=='__main__':
    from pprint import pprint

    g = RestConsumer(base_url='http://127.0.0.1:8000')
    users = g.userMgmt.users()[0]
    pprint(users)

    g = RestConsumer(base_url='http://127.0.0.1:8000')

    users : Response = g.userMgmt.customer()
    print(users)
    if users.status_code == 200:
        for user in users:
            pprint(user["email"])
    # adding new user
    #inputuserdata = {'username': 'rujwol', "password":"password"}
    #user = g.userMgmt.users.post(json = inputuserdata)
    #pprint(user)

    # pprint(users[1])
    # pprint(users[0])
