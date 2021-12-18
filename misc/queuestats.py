import requests


session = requests.Session()
session.auth = ("guest","guest")

auth = session.post("http://localhost:15672")
response = session.get("http://localhost:15672/api/queues/#/pyfi.queue1.proc1.do_this")
print(response.content)
