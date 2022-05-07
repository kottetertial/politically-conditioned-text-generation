import os
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()


class Env:
    ROOT_PREFIX = os.getenv("ROOT_PREFIX")
    EXTENSION_ID = os.getenv("EXTENSION_ID")
    PATH_TO_HTML = os.getenv("PATH_TO_HTML")
    PATH_TO_VPN_EXTENSION = os.getenv("PATH_TO_VPN_EXTENSION")


class SourceName:
    AMERICAN_PRESIDENCY_PROJECT = "American Presidency Project"
    WOMEN_POLITICAL_COMMUNICATION = "Archives of Women's Political Communication"
    BRITISH_POLITICAL_SPEECH = "British Political Speech"
    LABOUR_MANIFESTOS = "Archive of Labour Party Manifestos"
    LIBERAL_MANIFESTOS = "Liberal, SDP, Libdem Manifestos"
    CONSERVATIVE_MANIFESTOS = "Conservative Party Manifestos"


class SourceUrl:
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


class Symbol:
    SEP = "/"
    DASH = "—"
    EMPTY = ""


class Default:
    DATETIME = datetime(1970, 1, 1)
