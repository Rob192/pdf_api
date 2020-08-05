import json
import logging
import os

from pathlib import Path
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask import Flask
from flask import request, jsonify
from sqlitedict import SqliteDict
from pdf2txt import pdf2txt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

CWD = Path(os.getcwd())
UPLOAD_DIRECTORY = CWD  / "api_uploaded_files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def run_stats_request():
    data = {"success": False}
    try:
        stats_dict = dict(SqliteDict('./api_stats.sqlite', autocommit=True))
        data["success"] = True
        data["stats_info"] = stats_dict
    except Exception as e:
        logger.error(e)
    finally:
        return jsonify(data)


class Pdf2textAPI (Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('files')
        self.ALLOWED_EXTENSIONS = set(['pdf'])

    def allowed_file(self, filename):
        # this has changed from the original example because the original did not work for me
        return filename[-3:].lower() in self.ALLOWED_EXTENSIONS

    def post(self):
        data = {"success": False}
        stats_dict = SqliteDict('./api_stats.sqlite', autocommit=True)  # TODO: properly implement stats
        # output_types = ["pseudonymized", "tagged", "conll"]

        """Upload a file."""
        # try:
        file = request.files['file'] #get file in the request
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename) #make sure we have a proper filename
            logger.info(f'**found {filename}')
            full_filename = UPLOAD_DIRECTORY / filename
            file.save(full_filename) #saves pdf in folder
            pdf2txt(full_filename) #call pdf2txt on pdf
            with open(full_filename.with_suffix('.txt'), 'r', encoding='utf-8') as f:
                output = f.read()
            os.remove(full_filename)
            os.remove(full_filename.with_suffix('.txt'))
            data["text"] = str(output)
            data["success"] = True
            # TODO : add treatment for tabs
            # TODO : add spell checks
        stats_dict.close()
        return data


api.add_resource(Pdf2textAPI, '/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)