import sys
import pytest
import subprocess
import rethinkdb as rethink
from os import environ as env

# Why this works, I don't know. Blech.
sys.path.append(".")
sys.path.append("..")

from app.util import helpers

global token


def pytest_sessionstart(session):
    # Generate root access token
    from app import app
    if "ROOT_PASSWORD" not in app.config:
        password = input("Input the root password: ")
    else:
        password = app.config["ROOT_PASSWORD"]

    root_pass = subprocess.run("python3 gen.py --raw {} {}".format(
        password, "testing"
    ), stdout=subprocess.PIPE, shell=True)

    if root_pass.stdout.decode().rstrip() == "password":
        pytest.exit("\033[91mPASSWORD DOES NOT MATCH ROOT PASSWORD\033[0m")
    elif root_pass.stdout.decode().rstrip() == "account":
        pytest.exit("\033[91mROOT ACCOUNT IS NOT CONFIGURED\033[0m")
    else:
        global token
        token = root_pass.stdout.decode().rstrip()


def pytest_sessionfinish(session):
    r = rethink.connect(db="testing")
    for key in rethink.db("testing").table_list().run(r):
        if key not in ("keys", "users"):
            rethink.db("testing").table(key).delete().run(r)
        else:
            rethink.db("testing").table(key).filter(
                rethink.row["token"] != "root").delete().run(r)


@pytest.fixture
def app(request):
    from app import app
    global token
    app.config["TESTING"] = True
    app.config["RDB_DB"] = "testing"
    app.config["API_TOKEN"] = "root"
    app.config["API_KEY"] = token

    return app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def api_auth(app):
    return {
        "X-Auth-Token": app.config["API_TOKEN"],
        "X-Auth-Key": app.config["API_KEY"]
    }


@pytest.fixture
def command_data():
    return {
        "foo": {
            "name": "foo",
            "response": {
                "role": 0,
                "action": False,
                "target": None,
                "user": "",
                "message": [
                    {
                        "type": "text",
                        "data": "lol!",
                        "text": "lol!"
                    }
                ]
            }
        },
        "bar": {
            "name": "bar",
            "response": {
                "role": 0,
                "action": False,
                "target": None,
                "user": "",
                "message": [
                    {
                        "type": "emoji",
                        "data": "smile",
                        "text": ":)"
                    },
                    {
                        "type": "link",
                        "data": "https://google.com",
                        "text": "google.com"
                    }
                ]
            }
        }
    }
