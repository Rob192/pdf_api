import json
import logging
import os

from pathlib import Path
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask import Flask
from flask import request, jsonify
from sqlitedict import SqliteDict

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
        file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(f'**found {filename}')
            file.save(UPLOAD_DIRECTORY / filename)
            output = "dummy"
            # TODO: prepare output
            # output, analysis_ner_stats = prepare_output(text=text, tagger=TAGGER, output_type=output_type)
            # TODO: remove files after use
            data["text"] = filename
            data["success"] = True
            # stats_dict[:]
        # except Exception as e:
        #    logger.error(e)
        # finally:
        # logger.info(stopwatch.format_report(sw.get_last_aggregated_report()))
        if data["success"]:
            """ 
            update_stats(analysis_stats=stats_dict, analysis_ner_stats=analysis_ner_stats,
                         time_info=sw.get_last_aggregated_report(), output_type=output_type)
                         """
        # logger.info(json.dumps(dict(stats_dict), indent=4))
        stats_dict.close()
        return jsonify(data)


api.add_resource(Pdf2textAPI, '/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)