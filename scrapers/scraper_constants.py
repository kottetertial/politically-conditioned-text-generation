import os

from dotenv import load_dotenv

load_dotenv()


class Misc:
    # The American Presidency Project
    PARTY = "Party"
    PREFLABEL = "prefLabel"

    # The British Political Speech Archive
    LOCATION = "Location:"

    # Manifestos
    WIN = "Win"
    FULL_TEXT = "Full Manifesto text in a single long file"


class Tag:
    A = "a"
    B = "b"
    P = "p"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    LI = "li"
    TD = "td"
    TR = "tr"
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

    # The British Political Speech Archive
    RESULTS_TABLE = "results-table"
    SPEECH_CONTENT = "speech-content"
    SPEECH_SPEAKER = "speech-speaker"
    SPEECH_LOCATION = "speech-location"


class Selector:
    # The American Presidency Project
    LAST_CATEGORY = "div > ul > li.last.leaf.menu-mlid-10883"

    # The Iowa State University Archives of Women's Political Communication
    POST_CATEGORIES = "div.post-categories.post-meta"

    # VPN
    BUTTON_SELECTOR = os.getenv("BUTTON_SELECTOR")
