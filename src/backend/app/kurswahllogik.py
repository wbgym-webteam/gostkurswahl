# Liste aller Fächer
Kursliste = ["EN", "DE", "MA", "GE", "GEBI", "PB", "EK", "BI", "CH", "PH", "INF", "TK", "FR", "SN", "LA", "KU", "MU", "DS"]
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
# DS - Darstellendes Spiel

# Aufbau der Liste "taken_courses": [Wahlstufe, 1. LK, 2. LK, 1. GK, 2. GK, 3. GK, 4. GK, 5. GK, 6. GK]

def selection_level(taken_courses):
    if taken_courses[0] == 2:
        selection_choices = Leistungskurse(taken_courses)
    elif taken_courses[0] <= 6:
        selection_choices = Grundkurse(taken_courses)
    elif taken_courses[0] > 6:
        selection_choices = Wahlkurse(taken_courses)
    
def Leistungskurse(taken_courses):
    if taken_courses[1] == "EN":
        return ["Ma", "DE", "EK", "BI", "CH", "PH"]
    if taken_courses[1] == "DE":
        return ["Ma", "EK", "BI", "CH", "PH"]
    if taken_courses[1] == "MA":
        return ["EK", "BI", "CH", "PH"]

def Grundkurse(taken_courses):
    if taken_courses[0] == 3:
        return ["KU", "MU", "DS"]
    elif taken_courses[0] == 4:
        return ["GE", "GEBI"]
    elif taken_courses[0] == 5:
        if taken_courses[1] == "EN":
            if taken_courses[2] == "MA" or taken_courses[2] == "DE" or taken_courses[2] == "EK":
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
            if taken_courses[2] == "EK" or "MA":
                return ["BI", "CH", "PH"]
            else:
                return ["MA"]
        else:
            if taken_courses[2] == "EK":
                return ["BI", "CH", "PH"]
            else:
                return ["DE"]
        
def Wahlkurse(taken_curses):
    if taken_curses[0] == 7:
        if (taken_curses[1] == "EN" or taken_curses[1] == "MA") and taken_curses[2] == "EK":
            return ["DE"]
        elif taken_curses[1] == "DE" and taken_curses[2] == "EK":
            return ["MA"]
    Kursliste.remove(set(Kursliste) - set(taken_curses))
    return Kursliste
