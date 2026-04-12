import db_connector as dbc


class CourseSelector:
    
    # Aufbau der Liste taken_courses: [Wahlstufe, 1. LK, 2. LK, 1. GK, 2. GK, 3. GK, 4. GK, 5. GK, 6. GK]
    
    # Liste aller Fächer
    Kursliste = [
        "EN",
        "DE",
        "MA",
        "GE",
        "GEBI",
        "PB",
        "EK",
        "BI",
        "CH",
        "PH",
        "INF",
        "TK",
        "FR",
        "SN",
        "LA",
        "KU",
        "MU",
        "DS",
    ]
    # Ich hoffe das sind alle

    # Erklärungen der Abkürzungen:
    # EN - Englisch
    # DE - Deutsch
    # MA - Mathe
    # GE - Geschichte
    # GEBI - Geschichte Bilingual
    # PB - Politische Bildung
    # EK - Erdkunde
    # BI - Biologie
    # CH - Chemie
    # PH - Physik
    # INF - Informatik
    # TK - Technik
    # FR - Französisch
    # SN - Spanisch
    # LA - Latein
    # KU - Kunst
    # MU - Musik
    # DS - Darstellendes Spiel

    def __init__(self, db_module=dbc):
        self.db = db_module

    def selection_level(self, taken_courses, user_id):
        if taken_courses[0] == 2:
            selection_choices = self.leistungskurse(taken_courses)
        elif taken_courses[0] <= 6:
            selection_choices = self.grundkurse(taken_courses)
        else:
            selection_choices = self.wahlkurse(taken_courses)

        available_courses = self.db.retrieve_user_options(user_id)
        selection_choices = [c for c in selection_choices if c in available_courses]
        return selection_choices

    def leistungskurse(self, taken_courses):
        if taken_courses[1] == "EN":
            return ["MA", "DE", "EK", "BI", "CH", "PH"]
        if taken_courses[1] == "DE":
            return ["MA", "EK", "BI", "CH", "PH"]
        if taken_courses[1] == "MA":
            return ["EK", "BI", "CH", "PH"]
        return []

    def grundkurse(self, taken_courses):
        if taken_courses[0] == 3:
            return ["KU", "MU", "DS"]

        elif taken_courses[0] == 4:
            return ["GE", "GEBI"]

        elif taken_courses[0] == 5:
            if taken_courses[1] == "EN":
                if taken_courses[2] in ["MA", "DE", "EK"]:
                    return ["BI", "CH", "PH"]
                else:
                    return ["MA"]
            else:
                return ["EN", "FR", "LA", "SN"]

        else:
            if taken_courses[1] == "EN":
                if taken_courses[2] == "DE" or taken_courses[2] == "EK":
                    return ["MA"]
                else:
                    return ["DE"]

            elif taken_courses[1] == "DE":
                if taken_courses[2] == "EK" or taken_courses[2] == "MA":
                    return ["BI", "CH", "PH"]
                else:
                    return ["MA"]

            else:
                if taken_courses[2] == "EK":
                    return ["BI", "CH", "PH"]
                else:
                    return ["DE"]

    def wahlkurse(self, taken_courses):
        if taken_courses[0] == 7:
            if (taken_courses[1] == "EN" or taken_courses[1] == "MA") and taken_courses[2] == "EK":
                return ["DE"]
            elif taken_courses[1] == "DE" and taken_courses[2] == "EK":
                return ["MA"]

        Kursliste = [c for c in self.Kursliste if c not in taken_courses]
        return Kursliste

    def postwahlkurse(self, taken_courses, user_id):
        self.db.update_user_selection(user_id, taken_courses)