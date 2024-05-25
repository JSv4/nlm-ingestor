import base64
import io
import json
import os
import uuid
import zipfile

import nltk

from nlm_ingestor.datatypes.dicts import AnnotationLabelPythonType, OpenContractsExportDataJsonPythonType, \
    OpenContractsLabelSetType, OpenContractCorpusType
from nlm_ingestor.datatypes.enums import BlockTypes, LabelType

# Downloaded to C:\Users\scrud\AppData\Roaming\nltk_data
# nltk.download('punkt')
# nltk.download('stopwords')

import logging

logging.basicConfig(level=logging.INFO)
from nlm_ingestor.ingestor import pdf_ingestor

# doc_loc = 'sample.pdf'
doc_loc = "full NVCA.pdf"

def generate_labels() -> dict[str, AnnotationLabelPythonType]:
    annotation_label_jsons: dict[str, AnnotationLabelPythonType] = {}
    for feature_name in BlockTypes:
        annotation_label_jsons[feature_name] = {
            "id": uuid.uuid4().__str__(),
            "color": "gray",
            "description": "Nlm-ingestor region",
            "icon": "expand",
            "text": f"{feature_name} block",
            "label_type": LabelType.TOKEN_LABEL.value
        }
    return annotation_label_jsons
annotation_label_jsons = generate_labels()

corpus_data: OpenContractCorpusType = {
    "id": 1,
    "title": f"Nlm-ingestor test for {doc_loc}",
    "description": "Externally prepared 'corpus' by nlm-ingestor",
    "icon_data": "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",
    "icon_name": "icon.png",
    "creator": "scrudato@umich.edu",
    "label_set": 1
}

label_set: OpenContractsLabelSetType = {
    "id": 1,
    "title": "Nlmatics region labels",
    "description": "Nlmatics labelset for the Atticus Project's CUAD Corpus.",
    "icon_name": "f8282799-141f-4fed-9c0c-333f434e2831_AtticusProject.webp",
    "icon_data": "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",
    "creator": "scrudato@umich.edu"
}

os.environ["TIKA_SERVER_ENDPOINT"] = "http://localhost:9998"


# This would be called by ingestor_api.py if mime_type == "application/pdf"
ingestor = pdf_ingestor.PDFIngestor(doc_loc, {"apply_ocr": True, "calculate_opencontracts_data": True})
open_contracts_data = ingestor.open_contracts_data

with open(doc_loc, 'rb') as pdf_file:
    pdf_data = pdf_file.read()
    pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")

# Package labelset, document and annotations into OpenContracts format
data: OpenContractsExportDataJsonPythonType = {
    "annotated_docs": {doc_loc: open_contracts_data},
    "doc_labels": {},
    "text_labels": annotation_label_jsons,
    "corpus": corpus_data,
    "label_set": label_set
}

# package doc into OC Zip
output_bytes = io.BytesIO()
zip_file = zipfile.ZipFile(output_bytes, mode="w", compression=zipfile.ZIP_DEFLATED)
with open(doc_loc, 'rb') as pdf_file:

    # Write pdf file
    zip_file.writestr(doc_loc, pdf_file.read())

    # Write data file
    json_str = json.dumps(data) + "\n"
    json_bytes = json_str.encode("utf-8")
    zip_file.writestr("data.json", json_bytes)
    zip_file.close()

output_bytes.seek(io.SEEK_SET)
with open('nlm-processed-doc.zip', 'wb') as export_file:
    export_file.write(output_bytes.getvalue() )

with open("data.json", "w") as f:
    f.write(json.dumps(data, indent=4))
