# coding = utf-8

import urllib.request
import urllib.parse

# response = urllib.request.urlopen("https://www.baidu.com")
# print(response.read().decode('utf-8'))

#get request


#post request
data = bytes(urllib.parse.urlencode({"hello":"world"}), encoding="utf-8")
response = urllib.request.urlopen("http://httpbin.org/post", data=data)
#print(response.read().decode('utf-8'))

response = urllib.request.urlopen("http://httpbin.org/get")
print(response.read().decode('utf-8'))