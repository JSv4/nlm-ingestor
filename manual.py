import os
from tika import parser
from bs4 import BeautifulSoup

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nlm_ingestor.ingestor import patterns, line_parser, visual_ingestor
from nlm_ingestor.ingestor.visual_ingestor import visual_ingestor, table_parser, indent_parser, block_renderer, order_fixer



os.environ["TIKA_SERVER_ENDPOINT"] = "http://localhost:9998"

doc_loc = 'sample.pdf'
# doc_loc = '/Users/ambikasukla/Downloads/scansmpl.pdf'

# by default, we will turn off ocr as it is slow, use true here to parse ocr files
needs_ocr = False
timeout = 3000
if not needs_ocr:
    headers = {
        "X-Tika-OCRskipOcr": "true",
    }
    parsed = parser.from_file(doc_loc, xmlContent=True, requestOptions={'headers': headers, 'timeout': timeout})
else:
    print("ocr")
    headers = {
        "X-Tika-OCRskipOcr": "false",
        "X-Tika-OCRoutputType": "hocr",
        "X-Tika-OCRocrEngineMode": "3",
        "X-Tika-PDFExtractInlineImages":"false",
        "X-Tika-Timeout-Millis": str(100*timeout),
        "X-Tika-OCRtimeoutSeconds": str(timeout),
    }
    parsed = parser.from_file(doc_loc, xmlContent=True, requestOptions={'headers': headers, 'timeout': timeout})

html_str = parsed["content"]

soup = BeautifulSoup(str(parsed), "html.parser")
pages = soup.find_all("div", class_='page')
ocr_page = soup.find_all('div', class_="ocr_page", id='page_1')

block_renderer.HTML_DEBUG = True
visual_ingestor.LINE_DEBUG = False
indent_parser.LEVEL_DEBUG = False
indent_parser.NO_INDENT = False
visual_ingestor.MIXED_FONT_DEBUG = False
table_parser.TABLE_DEBUG = False
visual_ingestor.BLOCK_DEBUG = False
table_parser.TABLE_COL_DEBUG = False
table_parser.TABLE_HG_DEBUG = False
table_parser.TABLE_BOUNDS_DEBUG = False
visual_ingestor.HF_DEBUG = False
order_fixer.REORDER_DEBUG = False
visual_ingestor.MERGE_DEBUG = False
table_parser.TABLE_2_COL_DEBUG = False

# you can also let the visual ingestor only parse select pages
# but note that this will cause the document statistics to be incorrect
# and behaviour may not be consistent with what you see when you parse more pages or the entire document

# parsed_doc = visual_ingestor.Doc(pages[23:27], [])
parsed_doc = visual_ingestor.Doc(pages, [])
print(f"Parsed doc:\n\n{parsed_doc}")