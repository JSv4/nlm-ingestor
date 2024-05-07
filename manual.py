import os
from tika import parser
from bs4 import BeautifulSoup

import nltk

from nlm_ingestor.file_parser import markdown_parser

nltk.download('punkt')
nltk.download('stopwords')

import logging

logging.basicConfig(level=logging.INFO)

from nlm_ingestor.ingestor import patterns, line_parser, visual_ingestor, pdf_ingestor
from nlm_ingestor.ingestor.visual_ingestor import visual_ingestor, table_parser, indent_parser, block_renderer, \
    order_fixer

os.environ["TIKA_SERVER_ENDPOINT"] = "http://localhost:9998"

doc_loc = 'sample.pdf'

# This would be called by ingestor_api.py if mime_type == "application/pdf"
ingestor = pdf_ingestor.PDFIngestor(doc_loc, {"apply_ocr": True})
print(ingestor.return_dict)

# This then calls tika_html_doc = parse_pdf(doc_location, parse_options), which is part of
# pdf_ingestor.py...
# parse_options is a dict. if key apply_ocr set to True... will try to OCR

# BOTH ocr version and non-ocr version call:
# parsed_content = pdf_file_parser.parse_to_html(doc_location), but ocr adds do_ocr=True


ingestor = markdown_parser.MarkdownDocument('README.md')
print(ingestor.json_dict)