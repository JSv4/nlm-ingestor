import enum


class BlockTypes(str, enum.Enum):
    """
    Raw block types returned by nlm-ingestor
    """
    table_row = "table_row"
    para = "para"
    header = "header"
    list_item = "list_item"
    header_modified_to_para = "header_modified_to_para"
    parenthesized_hdr = "parenthesized_hdr"
    one_row_table = "one_row_table"

class LabelType(str, enum.Enum):
    DOC_TYPE_LABEL = "DOC_TYPE_LABEL"
    TOKEN_LABEL = "TOKEN_LABEL"
    RELATIONSHIP_LABEL = "RELATIONSHIP_LABEL"
    METADATA_LABEL = "METADATA_LABEL"
