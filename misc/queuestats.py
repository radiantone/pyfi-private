import requests
import json

session = requests.Session()
session.auth = ("guest","guest")

auth = session.post("http://localhost:15672")
#response = session.get("http://localhost:15672/api/queues/#/pyfi.queue1.proc1.do_this")
response = session.get("http://localhost:15672/api/queues") #/#/pyfi.queue3")
print(json.dumps(json.loads(response.content), indent=4))
