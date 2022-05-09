class Field:
    TEXT = "text"
    FILE_REF = "file_ref"


class Keywords:
    LIBERAL = ["Democrat", "Liberal"]
    CONSERVATIVE = ["Republican", "Conservative", "Federalist", "Whig"]

    SPOKEN = ["Spoken", "Oral", "Speech", "Briefing", "Radio", "Toast", "Conference", "Interview", "Address", "Chat",
              "Telephone", "TV", "Lecture", "Debate", "Television", "Exchange", "Commencement", "Discussion",
              "Dinner", "Breakfast", "Ads"]
    WRITTEN = ["Written", "Document", "Order", "Letter", "Veto", "Directive", "Article", "Proclamation", "Memoranda",
               "Notice", "Agreement", "Legislature", "Resignation", "Statement", "Message"]


class Party:
    LIBERAL = "Liberal"
    CONSERVATIVE = "Conservative"


class Type:
    SPOKEN = "Spoken"
    WRITTEN = "Written"
    AMBIGUOUS = "Ambiguous"
