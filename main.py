import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    render_template,
    flash,
    abort,
    send_from_directory,
)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.route("/")
@app.route("/<path:subpath>")
def show_directory(subpath=""):
    print(subpath)
    try:
        if os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"], subpath)):
            return send_from_directory(app.config["UPLOAD_FOLDER"], subpath)
        files = os.listdir(os.path.join(app.config["UPLOAD_FOLDER"], subpath))
    except FileNotFoundError as e:
        abort(404)
    is_directory = [
        os.path.isdir(os.path.join(app.config["UPLOAD_FOLDER"], subpath, f))
        for f in files
    ]
    return render_template(
        "index.html", files=files, is_directory=is_directory, subpath=subpath
    )


@app.route("/upload/", methods=["POST"])
@app.route("/upload/<path:subpath>", methods=["POST"])
def upload(subpath=""):
    if "file" not in request.files:
        flash("No file part", "error")
        return redirect("show_directory", subpath=subpath)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file", "error")
        return redirect(url_for("show_directory", subpath=subpath))
    if file:
        filename = secure_filename(file.filename)
        if os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"], subpath, filename)):
            flash("File with same name already exists.", "error")
        else:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], subpath, filename))
            flash("Uploaded file succesfully.", "success")
            return redirect(url_for("show_directory", subpath=subpath))
    return redirect(url_for("show_directory", subpath=subpath))


@app.route("/create-directory/", methods=["POST"])
@app.route("/create-directory/<path:subpath>", methods=["POST"])
def create_directory(subpath=""):
    dname = request.form.get("dname")
    try:
        os.mkdir(os.path.join(app.config["UPLOAD_FOLDER"], subpath, dname))
    except FileExistsError as e:
        flash("Directory already exists", "error")
        return redirect(url_for("show_directory", subpath=subpath))
    flash("Directory created successfully", "success")
    return redirect(url_for("show_directory", subpath=subpath))


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
