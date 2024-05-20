import logging
import nlm_ingestor.ingestion_daemon.config as cfg
import os
import tempfile
import traceback
from flask import Flask, request, jsonify, make_response
from werkzeug.utils import secure_filename
from nlm_ingestor.ingestor import ingestor_api
from nlm_utils.utils import file_utils

app = Flask(__name__)

# initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(cfg.log_level())

API_KEY = os.environ.get('API_KEY', None)
print(f"Ingestor API_KEY set to {API_KEY}")


@app.route('/', methods=['GET'])
def health_check():
    return 'Service is running', 200


@app.route('/api/parseDocument', methods=['POST'])
def parse_document(
        file=None,
        render_format: str = "all",
):
    # Verify API_KEY header
    api_key = request.headers.get('API_KEY')
    print(f"Request API_KEY: {api_key}")
    if isinstance(API_KEY, str) and api_key != API_KEY:
        return make_response(jsonify({"status": "fail", "reason": "Unauthorized"}), 401)

    render_format = request.args.get('renderFormat', 'all')
    use_new_indent_parser = request.args.get('useNewIndentParser', 'no')
    apply_ocr = request.args.get('applyOcr', 'no')
    calculate_opencontracts_data = request.args.get('calculate_opencontracts_data', "no")
    file = request.files['file']
    tmp_file = None
    try:
        parse_options = {
            "parse_and_render_only": True,
            "render_format": render_format,
            "use_new_indent_parser": use_new_indent_parser == "yes",
            "parse_pages": (),
            "apply_ocr": apply_ocr == "yes",
            "calculate_opencontracts_data": calculate_opencontracts_data == "yes"
        }
        # save the incoming file to a temporary location
        filename = secure_filename(file.filename)
        _, file_extension = os.path.splitext(file.filename)
        tempfile_handler, tmp_file = tempfile.mkstemp(suffix=file_extension)
        os.close(tempfile_handler)
        file.save(tmp_file)
        # calculate the file properties
        props = file_utils.extract_file_properties(tmp_file)
        logger.info(f"Parsing document: {filename}")
        return_dict, _ = ingestor_api.ingest_document(
            filename,
            tmp_file,
            props["mimeType"],
            parse_options=parse_options,
        )
        if tmp_file and os.path.exists(tmp_file):
            os.unlink(tmp_file)
        return make_response(
            jsonify({"status": 200, "return_dict": return_dict or {}}),
        )

    except Exception as e:
        print("error uploading file, stacktrace: ", traceback.format_exc())
        logger.error(
            f"error uploading file, stacktrace: {traceback.format_exc()}",
            exc_info=True,
        )
        status, rc, msg = "fail", 500, str(e)

    finally:
        if tmp_file and os.path.exists(tmp_file):
            os.unlink(tmp_file)
    return make_response(jsonify({"status": status, "reason": msg}), rc)


def main():
    logger.info("Starting ingestor service..")
    app.run(host="0.0.0.0", port=5001, debug=False)


if __name__ == "__main__":
    main()
