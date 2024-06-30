import sys, requests, json

# Usage:
# python3 GenAuth.py [url] [userid] [password]

url = sys.argv[1]
id = sys.argv[2]
password = sys.argv[3]


response = requests.post(url="{}/api/user/{}/authkey".format(url, id), json={
    "auth": password
})
authkey = json.loads(response.content.decode())

print(f"response: {authkey}")