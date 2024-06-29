from sanic import *
from sanic.response import text
from sanic_jinja2 import SanicJinja2
from jinja2 import FileSystemLoader
from datetime import datetime
import json, os
from functools import wraps
from api.jwt import verifyToken, createToken, extractToken


app = Sanic(__name__)
app.static("static", os.path.abspath("static"))

# Create jinja object
jinja = SanicJinja2(
    app, pkg_name="main", loader=FileSystemLoader(searchpath="template")
)

# Load configs
config = json.load(open("data/config.json", "r"))
app.config.URL = config["URL"]
app.config.KEY = config["KEY"] # Used for encrypting the jwt token
app.config.COOKIE = "razdor_dat"

# Create Decorators
def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = verifyToken(app.config.KEY, request.cookies.get(app.config.COOKIE))
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

@app.route("/")
@authorized()
async def index(request):
    return jinja.render("index.html", request, test="hey there!")

@app.route("/login")
async def login(request):
    return jinja.render("login.html")




@app.route("/cookie")
async def test(request):
    response = text("There's a cookie up in this response")
    response.add_cookie(
        "test1",
        "It worked!",
        max_age=604800,
        httponly=False
    )
    return response


if __name__ == "__main__":
    app.run(port=8888)
