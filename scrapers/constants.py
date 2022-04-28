import os
from dotenv import load_dotenv

load_dotenv()


class Misc:
    SEP = "/"
    EMPTY = ""
    ROOT_PREFIX = os.getenv("ROOT_PREFIX")

    # The American Presidency Project
    PARTY = "Party"
    PREFLABEL = "prefLabel"


class Source:
    # The American Presidency Project
    AMERICAN_PRESIDENCY_PROJECT = "https://www.presidency.ucsb.edu"
    DOCUMENTS = "/documents"


class Tag:
    A = "a"
    P = "p"
    H1 = "h1"
    H3 = "h3"
    LI = "li"
    DIV = "div"
    BODY = "body"


class Attribute:
    HREF = "href"

    # The American Presidency Project
    CONTENT = "content"
    PROPERTY = "property"


class ClassName:
    # The American Presidency Project
    ROW = "row"
    NEXT = "next"
    F_ITEM = "f-item"
    TAX_COUNT = "tax-count"
    GROUP_META = "group-meta"
    LABEL_ABOVE = "label-above"
    FIELD_TITLE = "field-title"
    VIEW_CONTENT = "view-content"
    DROPDOWN_MENU = "dropdown-menu"
    FIELD_DOC_COUNT = "field-doc-count"
    FIELD_SPOT_STATE = "field-spot-state"
    COL_MARGIN_TOP = "col-sm-4.margin-top"
    FIELD_DOCS_PERSON = "field-docs-person"
    FIELD_DOCS_CONTENT = "field-docs-content"
    DATE_DISPLAY_SINGLE = "date-display-single"


class Selector:
    # The American Presidency Project
    LAST_CATEGORY = "div > ul > li.last.leaf.menu-mlid-10883"


class TargetPath:
    # The American Presidency Project
    AMERICAN_PRESIDENCY_PROJECT_DOCS = "data/american_presidency_project/documents"
    AMERICAN_PRESIDENCY_PROJECT_PEOPLE = "data/american_presidency_project/people"
