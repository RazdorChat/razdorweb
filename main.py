from sanic import *
from sanic.response import text
from sanic_jinja2 import SanicJinja2
from jinja2 import FileSystemLoader
from datetime import datetime
import json, os
from functools import wraps
from api.jwt import verifyToken, createToken, extractToken
from api.account import *


app = Sanic(__name__)
app.static("static", os.path.abspath("static"))

# Create jinja object
jinja = SanicJinja2(
    app, pkg_name="main", loader=FileSystemLoader(searchpath="template")
)

# Load configs
config = json.load(open("data/config.json", "r"))
app.config.URL = config["URL"]
app.config.KEY = config["KEY"]  # Used for encrypting the jwt token
app.config.COOKIE = "razdor_dat"


# Create Decorators
# This one checks if they are trying to access the app without authorising
def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = verifyToken(
                app.config.KEY, request.cookies.get(app.config.COOKIE)
            )
            print(is_authorized)
            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return redirect("/login")

        return decorated_function

    return decorator

# this one checks if they are authorised and are trying to login/register
def IsAuthed():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = verifyToken(app.config.KEY, request.cookies.get(app.config.COOKIE))
            # Check if user is already authed and trying to login again
            if is_authorized:
                return redirect("/")
            else:
                response = await f(request, *args, **kwargs)
                return response
        return decorated_function
    return decorator

@app.route("/")
@authorized()
async def index(request):
    Ecookie = request.cookies.get(app.config.COOKIE)
    cookie = extractToken(app.config.KEY, Ecookie)
    print(cookie)
    return jinja.render("index.html", request, test="hey there you are {}!".format(cookie["user"]))


@app.route("/login", methods=["POST", "GET"])
@IsAuthed()
async def login(request):
    if request.method == "POST":
        username = request.form.get("username").split("#")
        password = request.form.get("password")
        try:
            verify = GenAuthUsername(username[0], username[1], password, app.config.URL)
        except IndexError:
            return jinja.render(
                "login.html",
                request,
                error="You have seemed to enter your username incorrectly.",
            )
        if verify["op"] == "Created.":
            payload = {
                "user":{
                    "id": verify["id"],
                    "username": username[0],
                    "discrim": username[1],
                    "password": password,
                    "authkey": verify["authentication"]
                }
            }
            
            cookie = createToken(app.config.KEY, payload)
            response = redirect("/")
            response.add_cookie(
                app.config.COOKIE,
                cookie,
                max_age=604800, # One week
                httponly = False
            )
            return response
                    
        elif verify["op"] == "void":
            return jinja.render(
                "login.html", request, error="Incorrect username or password."
            )

    return jinja.render("login.html", request, error=" ")

@app.route("/signup")
@IsAuthed()
def signup(requst, methods=["POST", "GET"]):
    if requst.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            CreateAcc(username, password, app.config.URL)
            

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
