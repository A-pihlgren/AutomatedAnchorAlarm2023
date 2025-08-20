import requests
import json
import io
import sched, time

s = sched.scheduler(time.time, time.sleep)
i = 300
starttime = time.time()
while True:
    print("json number: ", i)
    i += 1
    nameFile = "data" + str(i) + ".json"
    response = requests.get("https://api.vesselfinder.com/livedata?userkey=WS-4C858E2C-3EE")
    file = open(nameFile, "w")
    file.write(repr(response.json()))
    file.close()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
