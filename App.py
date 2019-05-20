import os

from flask import Flask, jsonify, request, abort, send_from_directory
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# default access page
@app.route("/")
def main():
    return abort(404)


# upload sected image and foward to processing page
@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/upload')

    # create image directory if not found
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from ..
    upload = request.files.getlist("file")[0]
    filename = upload.filename
    print("File name: {filename}".format(filename=filename))
    filename = str(filename).lower()
    print("File name: {filename}".format(filename=filename))

    # file support verification
    extension = os.path.splitext(filename)[1]
    if (extension == ".jpg") or (extension == ".png") or (extension == ".bmp"):
        print("File accepted")
    else:
        return abort(400)

    # save file
    destination = "".join([target, filename])
    print("File saved to : ", destination)
    upload.save(destination)

    # forward to processing page
    return send_image(filename)


@app.route('/wordcloud', methods=['POST'])
def generate_wordcloud():
    mask_image = request.files['mask_image']
    title = request.form['title']



    print(mask_image)
    return ""


# retrieve file from 'static/images' directory
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory("images/upload", filename)


# TODO: 걍 이미지의 주소를 전달해서 클라이언트가 읽도록 하자... json으로 response

if __name__ == "__main__":
    app.run(debug=True, host='', port=8000)
