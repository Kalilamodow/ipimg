import json
import os
import pathlib
import time
from urllib.parse import urlencode

import dotenv
from flask import Flask, redirect, request, send_file, send_from_directory

dotenv.load_dotenv()

script_directory = pathlib.Path(__file__).parent
data_directory = script_directory / "data"


def load_json(fp):
    with open(script_directory / fp, "r") as jfile:
        j = json.load(jfile)
    return j


def save_json(obj, fp):
    with open(script_directory / fp, "w") as f:
        json.dump(obj, f)


images = load_json(data_directory / "images.json")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

if not ADMIN_PASSWORD:
    raise Exception("Give me admin password please")


app = Flask(__name__)


@app.route("/")
def index_route():
    return request.remote_addr or ""


def admin_page_redir(pw: str, msg: str, err=False):
    args = {"pw": pw}

    if msg is not None:
        args["msg"] = msg
        args["msgiserror"] = "true" if err else "false"

    return redirect("/admin?" + urlencode(args))


@app.get("/admin")
def admin_route():
    pass_arg = request.args.get("pw")
    if pass_arg != ADMIN_PASSWORD:
        return f"""<form action="/admin" method="GET">
    {"wrong password!<br>" if pass_arg is not None else ""}
    <label for="pw">password: </label>
    <input type="text" name="pw" />

    <button>login</button>
</form>
"""

    return send_file(script_directory / "web" / "admin.html")


@app.post("/admin")
def admin_post_route():
    pass_arg = request.form.get("pw")
    if pass_arg != ADMIN_PASSWORD or pass_arg is None:
        return "401 unauthorized", 401

    if request.form.get("action-upload"):
        imgfile = request.files.get("img")
        if imgfile is None:
            return admin_page_redir(pass_arg, "Please select an image.", True)

        name_override = request.form.get("name-ovd")
        if name_override is not None and len(name_override) > 0:
            filename = name_override
        else:
            filename = imgfile.filename

        if filename is None or len(filename) == 0:
            return admin_page_redir(
                pass_arg, "The filename is nonexistent, somehow.", True
            )

        for image in images:
            if image["name"] == filename:
                return admin_page_redir(
                    pass_arg, "There's already an image with this name.", True
                )

        imgfile.save(data_directory / "images" / filename)
        images.append(
            {
                "name": filename,
                "created": round(time.time()),
                "accesses": [],
            }
        )

        save_json(images, data_directory / "images.json")

        return admin_page_redir(
            pass_arg, "Added image successfully. Filename: " + filename
        )

    return admin_page_redir(pass_arg, "Error: no action", True)


@app.route("/admin/get_images")
def admin_get_images():
    pass_arg = request.args.get("pw")
    if pass_arg != ADMIN_PASSWORD:
        return "unauthorized", 401

    return {"images": images}


@app.route("/i/<image>")
def image_route(image: str):
    global images
    noadd = request.args.get("noadd")
    if noadd != ADMIN_PASSWORD:
        newimages = []
        for previmage in images:
            if previmage["name"] != image:
                newimages.append(previmage)
                continue
            newimage = previmage.copy()
            newimage["accesses"].append(
                {"ip": request.remote_addr, "ts": round(time.time())}
            )
            newimages.append(newimage)
        images = newimages
        save_json(images, data_directory / "images.json")

    return send_from_directory(data_directory / "images", image)


if __name__ == "__main__":
    app.run(debug=True)
