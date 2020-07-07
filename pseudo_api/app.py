import json
import logging
import os

import stopwatch
from flair.models import SequenceTagger
from flask import Flask
from flask import request, jsonify
from sqlitedict import SqliteDict

from data_ETL import prepare_output, sw, update_stats

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

server = Flask(__name__)

# Env variables
PSEUDO_MODEL_PATH = os.environ.get('PSEUDO_MODEL_PATH', './model/best-model.pt')
TAGGER = SequenceTagger.load(PSEUDO_MODEL_PATH)


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


def run_pdf_request():
    data = {"success": False}
    stats_dict = SqliteDict('./api_stats.sqlite', autocommit=True) #TODO: properly implement stats
    #output_types = ["pseudonymized", "tagged", "conll"]

    """Upload a file."""
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(f'**found {filename}')
            file.save(UPLOAD_DIRECTORY / filename)
            output = "dummy"
            #TODO: prepare output
            #output, analysis_ner_stats = prepare_output(text=text, tagger=TAGGER, output_type=output_type)
            #TODO: remove files after use
            data["text"] = output
            data["success"] = True
            # stats_dict[:]
    except Exception as e:
        logger.error(e)
    finally:
        #logger.info(stopwatch.format_report(sw.get_last_aggregated_report()))
        if data["success"]:
            """ 
            update_stats(analysis_stats=stats_dict, analysis_ner_stats=analysis_ner_stats,
                         time_info=sw.get_last_aggregated_report(), output_type=output_type)
                         """
        #logger.info(json.dumps(dict(stats_dict), indent=4))
        stats_dict.close()
        return jsonify(data)


@server.route('/', methods=['GET', 'POST'])
def pseudonymize():
    #TODO: the request must be verified e.g. chef if a file is properly attached
    if request.method == 'GET':
        return 'The model is up and running. Send a POST request'
    else:
        return run_pdf_request()


@server.route('/api_stats/', methods=['GET'])
def stats():
    if request.method == 'POST':
        return 'The model is up and running. Send a GET request'
    else:
        return run_stats_request()
