import json
import os

from flask import Flask, jsonify, request, abort, send_from_directory
from flask_restful import Api, Resource, reqparse

from wcg import WCG

app = Flask(__name__)
api = Api(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# default access page
@app.route("/")
def main():
    return abort(404)


# upload sected image and foward to processing page
@app.route("/upload", methods=["POST"])
def upload_image():
    # create image directory if not found
    target = os.path.join(APP_ROOT, 'images')
    if not os.path.isdir(target):
        os.mkdir(target)
    target = os.path.join(target, 'upload/')
    if not os.path.isdir(target):
        os.mkdir(target)

    # retrieve file from ..
    upload = request.files.getlist("image")[0]
    filename = upload.filename
    print("File name: {filename}".format(filename=filename))
    filename = str(filename).lower()
    print("File name: {filename}".format(filename=filename))

    # file support verification
    extension = os.path.splitext(filename)[1]
    if (extension == ".jpg") or (extension == ".jpeg") or (extension == ".png") or (extension == ".bmp"):
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
    directory_path = os.path.join(APP_ROOT, 'images/')
    directory_path = os.path.join(directory_path, 'upload/')

    mask_upload = request.files.getlist("mask_image")[0]
    mask_filename = str(mask_upload.filename).lower()
    print("File name: {filename}".format(filename=mask_filename))

    extension = os.path.splitext(mask_filename)[1]
    if (extension == ".jpg") or (extension == ".jpeg") or (extension == ".png") or (extension == ".bmp"):
        print("File accepted")
    else:
        return abort(400)

    # Save file
    mask_image_path = "".join([directory_path, mask_filename])
    print(" path : {path}".format(path=mask_image_path))
    mask_upload.save(mask_image_path)

    title = request.form['title']
    data = request.form['data']
    font = request.form['font']

    wc = WCG(title=title, data=data, font=font, mask_image_path=mask_image_path)
    wordCloud_path = wc.generate()

    print(wordCloud_path)
    return send_wordcloud(wordCloud_path)


# retrieve file from 'static/images' directory
@app.route('/static/mask/<filename>')
def send_image(filename):
    return send_from_directory("images/upload", filename)


@app.route('/static/wordcloud/<filename>')
def send_wordcloud(filename):
    print(filename)
    return send_from_directory("images/wordcloud", filename)


@app.route('/static/font/<filename>', methods=['GET'])
def send_font(filename):
    print("send_font: " + filename)
    return send_from_directory("fonts/static", filename=filename)


@app.route('/static/font/', methods=['GET'])
def send_font_list():
    print("send_font_list")
    font_dir = './fonts/static'
    font_file_list = os.listdir(font_dir)
    font_list = []
    for font_file in font_file_list:
        font = {"name":font_file.replace('.ttc', '').replace('.ttf', '').replace('.otf', ''),"path": font_file}
        font_list.append(font)
    print('font_list created.')

    font_json = jsonify(font_list)
    print('font_json created.')

    return font_json

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
