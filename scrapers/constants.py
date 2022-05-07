import os
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()


class Misc:
    SEP = "/"
    DASH = "—"
    EMPTY = ""
    DEFAULT_DATETIME = datetime(1970, 1, 1)

    # The American Presidency Project
    PARTY = "Party"
    PREFLABEL = "prefLabel"

    # The British Political Speech Archive
    LOCATION = "Location:"

    # Manifestos
    WIN = "Win"
    FULL_TEXT = "Full Manifesto text in a single long file"


class Env:
    ROOT_PREFIX = os.getenv("ROOT_PREFIX")
    EXTENSION_ID = os.getenv("EXTENSION_ID")
    PATH_TO_HTML = os.getenv("PATH_TO_HTML")
    PATH_TO_VPN_EXTENSION = os.getenv("PATH_TO_VPN_EXTENSION")


class Source:
    # The American Presidency Project
    AMERICAN_PRESIDENCY_PROJECT = "https://www.presidency.ucsb.edu"
    DOCUMENTS = "/documents"

    # The Iowa State University Archives of Women's Political Communication
    WOMEN_POLITICAL_COMMUNICATION = "https://awpc.cattcenter.iastate.edu"
    SPEAKERS = "/speakers"

    # The British Political Speech Archive
    BRITISH_POLITICAL_SPEECH = "http://www.britishpoliticalspeech.org"
    ARCHIVE = "/speech-archive.htm"

    # Party Manifestos
    LABOUR = "http://www.labour-party.org.uk/manifestos/"
    LIBERAL = "http://www.libdemmanifesto.com/"
    CONSERVATIVE = "http://www.conservativemanifesto.com/"


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

    # The British Political Speech Archive
    BRITISH_POLITICAL_SPEECH_DOCS = "{}/british_political_speech/{}".format(DATA, DOCUMENTS)

    # Manifestos
    MANIFESTOS = "{}/manifestos/{}".format(DATA, DOCUMENTS)
