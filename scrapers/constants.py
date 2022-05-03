import os
from dotenv import load_dotenv

load_dotenv()


class Misc:
    SEP = "/"
    DASH = "—"
    EMPTY = ""
    ROOT_PREFIX = os.getenv("ROOT_PREFIX")

    # The American Presidency Project
    PARTY = "Party"
    PREFLABEL = "prefLabel"


class Source:
    # The American Presidency Project
    AMERICAN_PRESIDENCY_PROJECT = "https://www.presidency.ucsb.edu"
    DOCUMENTS = "/documents"

    # The Iowa State University Archives of Women's Political Communication
    WOMEN_POLITICAL_COMMUNICATION = "https://awpc.cattcenter.iastate.edu"
    SPEAKERS = "/speakers"


class Tag:
    A = "a"
    P = "p"
    H1 = "h1"
    H3 = "h3"
    LI = "li"
    TD = "td"
    DIV = "div"
    BODY = "body"
    TABLE = "table"


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

    # The Iowa State University Archives of Women's Political Communication
    PARTY = "party"
    WEBSITE = "website"
    ARTICLES = "articles"
    POST_CONTENT = "post-content"
    PROFILE_INFO = "profile-info"
    PROFILES_LIST = "profiles-list"
    WOMENSPEECH_DATE = "womenspeech-date"


class Selector:
    # The American Presidency Project
    LAST_CATEGORY = "div > ul > li.last.leaf.menu-mlid-10883"

    # The Iowa State University Archives of Women's Political Communication
    POST_CATEGORIES = "div.post-categories.post-meta"


# TODO: replace concatenation with formatting everywhere
# TODO: create directories automatically
class TargetPath:
    DATA = "data"
    PEOPLE = "people"
    DOCUMENTS = "documents"

    # The American Presidency Project
    AMERICAN_PRESIDENCY_PROJECT_PEOPLE = "{}/american_presidency_project/{}".format(DATA, PEOPLE)
    AMERICAN_PRESIDENCY_PROJECT_DOCS = "{}/american_presidency_project/{}".format(DATA, DOCUMENTS)

    # The Iowa State University Archives of Women's Political Communication
    WOMEN_POLITICAL_COMMUNICATION_PEOPLE = "{}/women_political_communication/{}".format(DATA, PEOPLE)
    WOMEN_POLITICAL_COMMUNICATION_DOCS = "{}/women_political_communication/{}".format(DATA, DOCUMENTS)
