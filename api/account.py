# Functions to manage account creation and deletion, and authkey generation from user cookies

import requests, json


def CreateAcc(username: str, password: str, url: str):
    Furl = "{}/api/user/create".format(url)  # Add correct url
    try:
        Request = requests.post(
            url=Furl, json={"password": password, "username": username}
        )
        Response = json.loads(Request.content.decode())
    except:
        return "ERR"

    return Response


# :(
def DeleteAcc(id: str, auth: str, url: str):
    Furl = "{}/api/user/{}/delete".format(url, id)
    try:
        Request = requests.post(url=Furl, json={"auth": auth})
        Response = json.loads(Request.content.decode())
    except:
        return "ERR"
    return Response

# Generate an auth from the users browser cookies
def GenAuth(id: str, password: str, url: str):
    Furl = "{}/api/user/{}/authkey".format(url, id)
    try:
        Request = requests.post(url=Furl, json={"auth": password})
        Response = json.loads(Request.content.decode())
    except:
        return "ERR"
    return Response
