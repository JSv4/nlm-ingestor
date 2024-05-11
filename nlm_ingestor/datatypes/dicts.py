from typing import TypedDict, Union, Optional


class PawlsPageBoundaryPythonType(TypedDict):
    """
    This is what a PAWLS Page Boundary obj looks like
    """

    width: float
    height: float
    index: int


class PawlsTokenPythonType(TypedDict):
    """
    This is what an actual PAWLS token looks like.
    """

    x: float
    y: float
    width: float
    height: float
    text: str


class PawlsPagePythonType(TypedDict):
    """
    Pawls files are comprised of lists of jsons that correspond to the
    necessary tokens and page information for a given page. This describes
    the data shape for each of those page objs.
    """

    page: PawlsPageBoundaryPythonType
    tokens: list[PawlsTokenPythonType]


class BoundingBoxPythonType(TypedDict):
    """
    Bounding box for pdf box on a pdf page
    """

    top: int
    bottom: int
    left: int
    right: int


class TokenIdPythonType(TypedDict):
    """
    These are how tokens are referenced in annotation jsons.
    """

    pageIndex: int
    tokenIndex: int


class OpenContractsSinglePageAnnotationType(TypedDict):
    """
    This is the data shape for our actual annotations on a given page of a pdf.
    In practice, annotations are always assumed to be multi-page, and this means
    our annotation jsons are stored as a dict map of page #s to the annotation data:

    Dict[int, OpenContractsSinglePageAnnotationType]

    """

    bounds: BoundingBoxPythonType
    tokensJsons: list[TokenIdPythonType]
    rawText: str


class OpenContractsAnnotationPythonType(TypedDict):
    """
    Data type for individual Open Contract annotation data type converted
    into JSON. Note the models have a number of additional fields that are not
    relevant for import/export purposes.
    """

    id: Optional[Union[str, int]]  # noqa  # fmt: off
    annotationLabel: str
    rawText: str
    page: int
    annotation_json: dict[Union[int, str], OpenContractsSinglePageAnnotationType]


class OpenContractsDocAnnotations(TypedDict):
    # Can have multiple doc labels. Want array of doc label ids, which will be
    # mapped to proper objects after import.
    doc_labels: list[str]

    # The annotations are stored in a list of JSONS matching OpenContractsAnnotationPythonType
    labelled_text: list[OpenContractsAnnotationPythonType]


class OpenContractDocExport(OpenContractsDocAnnotations):
    """
    Eech individual documents annotations are exported and imported into
    and out of jsons with this form. Inherits doc_labels and labelled_text
    from OpenContractsDocAnnotations
    """

    # Document title
    title: str

    # Document text
    content: str

    # Document description
    description: Optional[str]

    # Documents PAWLS parse file contents (serialized)
    pawls_file_content: list[PawlsPagePythonType]

    # We need to have a page count for certain analyses
    page_count: int
