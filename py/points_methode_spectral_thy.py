# ==========================================================================
#   Python #1 - Extraction HOL + Injection SQLite
#   Projet   : methode_spectral.thy - Pipeline de validation HOL
#   Auteur   : Philippe Thomas Savard
#   Fichier  : points_methode_spectral_thy.py
#   Base     : C:\\pipeline_thonnys_theorie_des_nombres\\
#   Produit  : methode_spectral_hol.db + rapport_spectral_points.txt + .json
# ==========================================================================

import re
import json
import sqlite3
import os

# =========================================================================
# CONFIGURATION
# =========================================================================
BASE_DIR  = r"C:\pipeline_thonnys_theorie_des_nombres"
THY_FILE  = os.path.join(BASE_DIR, "methode_spectral.thy")
DB_FILE   = os.path.join(BASE_DIR, "methode_spectral_hol.db")
TXT_FILE  = os.path.join(BASE_DIR, "rapport_spectral_points.txt")
JSON_FILE = os.path.join(BASE_DIR, "rapport_spectral_points.json")

# =========================================================================
# ARCHITECTURE ENSEMBLE = 1  (10 noeuds logiques - Regle Savard)
# =========================================================================
SECTIONS_ARCHITECTURE = [
    {
        "code": "ENSEMBLE",
        "label": "Ensemble = 1  (Theoreme d'unification Pont Savard)",
        "description": (
            "Cercle le plus grand. "
            "Aboutit au theoreme synthese_pont_savard : RsP = Re = 1/2 VRAI."
        ),
        "parent": None,
        "hol_anchor": "synthese_pont_savard",
        "ligne_anchor": 4154,
    },
    {
        "code": "1/x",
        "label": "1/x - Fonction zeta de Riemann",
        "description": "Decomposee en 1/y1 + 1/y2 + 1/y3.",
        "parent": "ENSEMBLE",
        "hol_anchor": "ensemble_savard",
        "ligne_anchor": 3987,
    },
    {
        "code": "1/t",
        "label": "1/t - Equation psi_savard (pont Tchebychev <-> Methode Spectrale)",
        "description": (
            "psi_savard est le pont fonctionnel entre Tchebychev et la Methode Spectrale. "
            "Lie via x^p/p et 2^n/SB_n. Section XIII.1-XIII.2."
        ),
        "parent": "ENSEMBLE",
        "hol_anchor": "psi_savard",
        "ligne_anchor": 3671,
    },
    {
        "code": "1/ms",
        "label": "1/ms - Methode Spectrale (decomposee en 1/ms1 + 1/ms2 + 1/ms3)",
        "description": "La Methode Spectrale de Savard dans son integralite operationnelle.",
        "parent": "ENSEMBLE",
        "hol_anchor": "RsP_universel_entier_naturel",
        "ligne_anchor": 4105,
    },
    {
        "code": "1/y1",
        "label": "1/y1 - Composante Tchebychev (zeros non-triviaux -> positions P)",
        "description": (
            "Zeros non-triviaux de zeta determinent la position de tous les premiers P. "
            "Section XIII.3."
        ),
        "parent": "1/x",
        "hol_anchor": "methode_spectrale_exclusivite_P",
        "ligne_anchor": 3880,
    },
    {
        "code": "1/y2",
        "label": "1/y2 - Droite critique Re(rho) = 1/2",
        "description": (
            "Hypothese de Riemann : tous les zeros non-triviaux ont Re = 1/2. "
            "Section XIII.5 : locale ensemble_savard, hypothese_critique."
        ),
        "parent": "1/x",
        "hol_anchor": "alignement_central",
        "ligne_anchor": 4004,
    },
    {
        "code": "1/y3",
        "label": "1/y3 - Equation de Tchebychev (psi classique)",
        "description": (
            "Equation de Tchebychev classique. Validee numeriquement pour x=30,98,228."
        ),
        "parent": "1/x",
        "hol_anchor": "psi_savard_expanded",
        "ligne_anchor": 3709,
    },
    {
        "code": "1/ms1",
        "label": "1/ms1 - Reconstruction du i-ieme premier (Operation 1)",
        "description": (
            "Suites SA/SB, digamma_calc, prime_equation_prime_i, RsP_generic_constant. "
            "Sections I a XI.bis."
        ),
        "parent": "1/ms",
        "hol_anchor": "prime_equation_prime_i",
        "ligne_anchor": 754,
    },
    {
        "code": "1/ms2",
        "label": "1/ms2 - Exclusion stricte des composes C (Preuve par l'absurde)",
        "description": (
            "Trois piliers : composite_not_prime_i, composite_no_reconstruction_position, "
            "composite_pair_no_rsp_positions."
        ),
        "parent": "1/ms",
        "hol_anchor": "composite_not_prime_i",
        "ligne_anchor": 1821,
    },
    {
        "code": "1/ms3",
        "label": "1/ms3 - Rapport spectral RsP = 1/2 pour l'ensemble P (Operation 3)",
        "description": (
            "Regime central k=2 : RsP(n1,n2) = 1/2 pour tout n1!=n2, n1>=1, n2>=1."
        ),
        "parent": "1/ms",
        "hol_anchor": "RsP_un_demi_general",
        "ligne_anchor": 386,
    },
]

# =========================================================================
# CONCORDANCES C1 / C2 / C3
# =========================================================================
CONCORDANCES = [
    {
        "code": "C1",
        "section_source": "1/y1",
        "section_cible": "1/t",
        "type_relation": "PONT_VERS",
        "description": (
            "C1 : Tchebychev = psi_savard. "
            "Les deux traitent du meme sujet via x^p/p et 2^n/SB_n. "
            "Le reste des deux equations est identique : log(2Pi)-0.5*log(1-x^-2)."
        ),
        "hol_lemmes": "psi_savard_expanded, psi_savard_at_10_30_expanded, rapport_zeta_savard_at_10",
    },
    {
        "code": "C2",
        "section_source": "1/y3",
        "section_cible": "1/ms1",
        "type_relation": "VALIDE",
        "description": (
            "C2 : zeros non-triviaux = valeurs de n = positions des P. "
            "La methode spectrale et la fonction zeta determinent les memes positions."
        ),
        "hol_lemmes": "prime_equation_prime_i, RsP_generic_constant, RsP_universel_entier_naturel",
    },
    {
        "code": "C3",
        "section_source": "1/y2",
        "section_cible": "1/ms3",
        "type_relation": "VALIDE",
        "description": (
            "C3 : Re(rho) = 1/2 = RsP = 1/2. "
            "La droite critique de Riemann s'aligne sur le rapport spectral central."
        ),
        "hol_lemmes": "synthese_pont_savard, alignement_central, pont_spectral_direct_final, Re_droite_critique",
    },
]

# =========================================================================
# MOTIFS DE DETECTION HOL
# =========================================================================
PATTERNS = [
    ("section",         re.compile(r'^section\s+"([^"]+)"')),
    ("subsection",      re.compile(r'^subsection\s+(?:\\<open>|")([^"\\<]+)(?:\\<close>|")')),
    ("text",            re.compile(r'^text\s+\\<open>')),
    ("locale",          re.compile(r'^locale\s+([A-Za-z0-9_]+)')),
    ("interpretation",  re.compile(r'^interpretation\s+([A-Za-z0-9_]+)')),
    ("definition",      re.compile(r'^definition\s+(?:\(in\s+[A-Za-z0-9_]+\)\s+)?([A-Za-z0-9_]+)')),
    ("lemma",           re.compile(r'^lemma\s+(?:\(in\s+[A-Za-z0-9_]+\)\s+)?([A-Za-z0-9_]+)')),
    ("theorem",         re.compile(r'^theorem\s+(?:\(in\s+[A-Za-z0-9_]+\)\s+)?([A-Za-z0-9_]+)')),
    ("corollary",       re.compile(r'^corollary\s+([A-Za-z0-9_]+)')),
    ("axiomatization",  re.compile(r'^axiomatization\s+where')),
    ("consts",          re.compile(r'^consts')),
    ("typedecl",        re.compile(r'^typedecl\s+([A-Za-z0-9_]+)')),
    ("fun",             re.compile(r'^fun\s+([A-Za-z0-9_]+)')),
    ("abbreviation",    re.compile(r'^abbreviation\s+([A-Za-z0-9_]+)')),
]

# =========================================================================
# AFFECTATION A LA SECTION LOGIQUE (par plages de lignes)
# =========================================================================
def section_logique_pour_ligne(n, nom, type_obj):
    if nom in ("synthese_pont_savard", "pont_spectral_direct_final",
               "ensemble_savard_satisfaisable", "Re_droite_critique",
               "RsP_universel_entier_naturel"):
        return "ENSEMBLE"
    if 3514 <= n <= 3853: return "1/t"
    if 3854 <= n <= 3943: return "1/y1"
    if 3944 <= n <= 4164: return "1/y2"
    if nom in ("psi_savard_expanded", "psi_savard_at_10_30_expanded",
               "psi_savard_at_25_98_expanded", "psi_savard_at_49_228_expanded",
               "rapport_zeta_savard_at_10", "rapport_zeta_savard_at_25",
               "rapport_zeta_savard_at_49"):
        return "1/y3"
    if 1810 <= n <= 2138: return "1/ms2"
    if (381 <= n <= 547) or (925 <= n <= 1040) or (2947 <= n <= 3245):
        return "1/ms3"
    if nom in ("RsP_un_demi_general", "RsP_un_tiers_constant",
               "RsP_un_quart_constant", "RsP_generic_constant",
               "algebriquement_incoherent_local", "coherence_numerique_reelle_P",
               "RsP_1_3", "RsP_1_4", "RsP_k", "RsP_neg_k",
               "regime_1_2", "regime_1_3", "regime_1_4"):
        return "1/ms3"
    if (353 <= n <= 1809) or (2139 <= n <= 2946) or (3246 <= n <= 3513):
        return "1/ms1"
    if n <= 352: return "ENSEMBLE"
    if n >= 4165: return "ENSEMBLE"
    return "1/ms1"

# =========================================================================
# EXTRACTION DES POINTS HOL
# =========================================================================
def extraire_points(thy_text):
    points = []
    lignes = thy_text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    compteur = 1
    texte_c = axiom_c = const_c = 1
    current_section = current_subsection = ""

    for i, ligne in enumerate(lignes):
        ls  = ligne.strip()
        ln  = i + 1
        if "License" in ligne or "Apache" in ligne:
            continue
        if ls.startswith("(*"):
            continue
        for type_obj, pattern in PATTERNS:
            m = pattern.match(ls)
            if not m:
                continue
            if type_obj == "text":
                nom = "text_block_" + str(texte_c); texte_c += 1
            elif type_obj == "axiomatization":
                nom = "axiomatization_bloc_" + str(axiom_c); axiom_c += 1
            elif type_obj == "consts":
                nom = "consts_bloc_" + str(const_c); const_c += 1
            else:
                try:
                    nom = m.group(1).strip()
                except Exception:
                    nom = type_obj
            if type_obj == "section":
                current_section = nom
                current_subsection = ""
            elif type_obj == "subsection":
                current_subsection = nom
            sl = section_logique_pour_ligne(ln, nom, type_obj)
            points.append({
                "id": compteur,
                "type": type_obj,
                "nom": nom,
                "ligne": ln,
                "section_thy": current_section,
                "subsection_thy": current_subsection,
                "section_logique": sl,
            })
            compteur += 1
            break
    return points

# =========================================================================
# RELATIONS ENTRE POINTS HOL
# =========================================================================
def construire_relations(points):
    relations = []
    rid = 1
    last_def_by_section = {}

    for p in points:
        sec = p["section_logique"]
        if p["type"] in ("lemma", "corollary") and sec in last_def_by_section:
            relations.append({
                "id": rid,
                "point_source_id": p["id"],
                "point_cible_id": last_def_by_section[sec]["id"],
                "type_relation": "DEPEND_DE",
                "description": p["nom"] + " depend de " + last_def_by_section[sec]["nom"],
            })
            rid += 1
        if p["type"] == "theorem" and sec in last_def_by_section:
            relations.append({
                "id": rid,
                "point_source_id": p["id"],
                "point_cible_id": last_def_by_section[sec]["id"],
                "type_relation": "VALIDE",
                "description": p["nom"] + " valide " + last_def_by_section[sec]["nom"],
            })
            rid += 1
        if p["type"] == "definition":
            last_def_by_section[sec] = p

    RELATIONS_CLES = [
        ("RsP_un_demi_general",                  "synthese_pont_savard",           "CONDUIT_A"),
        ("RsP_universel_entier_naturel",          "synthese_pont_savard",           "CONDUIT_A"),
        ("prime_equation_prime_i",               "synthese_pont_savard",           "CONDUIT_A"),
        ("reconstruction_premier_pos",           "prime_equation_prime_i",         "DEPEND_DE"),
        ("composite_not_prime_i",                "synthese_pont_savard",           "CONDUIT_A"),
        ("composite_no_reconstruction_position", "composite_not_prime_i",          "DEPEND_DE"),
        ("composite_pair_no_rsp_positions",      "composite_not_prime_i",          "DEPEND_DE"),
        ("psi_savard",                           "methode_spectrale_exclusivite_P","PONT_VERS"),
        ("alignement_central",                   "RsP_un_demi_general",            "VALIDE"),
        ("conclusion_ensemble",                  "synthese_pont_savard",           "CONDUIT_A"),
        ("RsP_generic_constant",                 "RsP_un_demi_general",            "GENERALISE"),
        ("RsP_generic_constant",                 "RsP_un_tiers_constant",          "GENERALISE"),
        ("RsP_generic_constant",                 "RsP_un_quart_constant",          "GENERALISE"),
        ("pont_spectral_direct_final",           "synthese_pont_savard",           "DEPEND_DE"),
        ("Re_droite_critique",                   "synthese_pont_savard",           "DEPEND_DE"),
        ("ensemble_savard_satisfaisable",        "synthese_pont_savard",           "VALIDE"),
        ("psi_savard_at_10_30_expanded",         "psi_savard_expanded",            "DEPEND_DE"),
        ("psi_savard_at_25_98_expanded",         "psi_savard_expanded",            "DEPEND_DE"),
        ("psi_savard_at_49_228_expanded",        "psi_savard_expanded",            "DEPEND_DE"),
        ("digamma_calc_29",                      "prime_equation_prime_i",         "DEPEND_DE"),
        ("digamma_calc_31",                      "prime_equation_prime_i",         "DEPEND_DE"),
        ("digamma_calc_37",                      "prime_equation_prime_i",         "DEPEND_DE"),
        ("digamma_calc_41",                      "prime_equation_prime_i",         "DEPEND_DE"),
        ("preuve_premier_947",                   "prime_equation_prime_i",         "DEPEND_DE"),
        ("preuve_premier_227",                   "prime_equation_prime_i",         "DEPEND_DE"),
        ("SA_eq_regime_1_2_A_pos",               "RsP_generic_constant",           "DEPEND_DE"),
        ("SB_eq_regime_1_2_B_pos",               "RsP_generic_constant",           "DEPEND_DE"),
    ]
    nom_vers_id = {p["nom"]: p["id"] for p in points}
    for (src_nom, cib_nom, type_rel) in RELATIONS_CLES:
        src_id = nom_vers_id.get(src_nom)
        cib_id = nom_vers_id.get(cib_nom)
        if src_id and cib_id:
            relations.append({
                "id": rid,
                "point_source_id": src_id,
                "point_cible_id": cib_id,
                "type_relation": type_rel,
                "description": src_nom + " --[" + type_rel + "]--> " + cib_nom,
            })
            rid += 1
    return relations

# =========================================================================
# CREATION BASE SQLITE
# =========================================================================
def creer_base_sqlite(db_path, sections, points, relations, concordances):
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    cur.execute("""CREATE TABLE sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        label TEXT NOT NULL,
        description TEXT,
        parent TEXT,
        hol_anchor TEXT,
        ligne_anchor INTEGER,
        FOREIGN KEY (parent) REFERENCES sections(code))""")
    for s in sections:
        cur.execute(
            "INSERT INTO sections (code,label,description,parent,hol_anchor,ligne_anchor) VALUES (?,?,?,?,?,?)",
            (s["code"], s["label"], s["description"],
             s.get("parent"), s.get("hol_anchor"), s.get("ligne_anchor")))

    cur.execute("""CREATE TABLE points (
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        nom TEXT NOT NULL,
        ligne INTEGER NOT NULL,
        section_thy TEXT,
        subsection_thy TEXT,
        section_logique TEXT NOT NULL,
        FOREIGN KEY (section_logique) REFERENCES sections(code))""")
    for p in points:
        cur.execute("INSERT INTO points VALUES (?,?,?,?,?,?,?)",
            (p["id"], p["type"], p["nom"], p["ligne"],
             p["section_thy"], p["subsection_thy"], p["section_logique"]))

    cur.execute("""CREATE TABLE relations (
        id INTEGER PRIMARY KEY,
        point_source_id INTEGER NOT NULL,
        point_cible_id INTEGER NOT NULL,
        type_relation TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (point_source_id) REFERENCES points(id),
        FOREIGN KEY (point_cible_id)  REFERENCES points(id))""")
    for r in relations:
        cur.execute("INSERT INTO relations VALUES (?,?,?,?,?)",
            (r["id"], r["point_source_id"], r["point_cible_id"],
             r["type_relation"], r["description"]))

    cur.execute("""CREATE TABLE concordances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL UNIQUE,
        section_source TEXT NOT NULL,
        section_cible TEXT NOT NULL,
        type_relation TEXT NOT NULL,
        description TEXT,
        hol_lemmes TEXT,
        FOREIGN KEY (section_source) REFERENCES sections(code),
        FOREIGN KEY (section_cible)  REFERENCES sections(code))""")
    for c in concordances:
        cur.execute(
            "INSERT INTO concordances (code,section_source,section_cible,type_relation,description,hol_lemmes) VALUES (?,?,?,?,?,?)",
            (c["code"], c["section_source"], c["section_cible"],
             c["type_relation"], c["description"], c["hol_lemmes"]))

    conn.commit()
    conn.close()

# =========================================================================
# RAPPORT TEXTE NUMEROTE
# =========================================================================
def generer_rapport_texte(points, sections, concordances):
    lignes = [
        "=" * 80,
        "  RAPPORT HOL - methode_spectral.thy",
        "  Auteur : Philippe Thomas Savard",
        "  Architecture : Ensemble = 1/x + 1/t + 1/ms",
        "=" * 80,
    ]
    for sec in sections:
        pts_sec = [p for p in points if p["section_logique"] == sec["code"]]
        if not pts_sec:
            continue
        lignes += [
            "",
            "-" * 70,
            "  SECTION : " + sec["code"] + " - " + sec["label"],
            "  Ancre HOL : " + str(sec.get("hol_anchor", "N/A")) +
            " (ligne " + str(sec.get("ligne_anchor", "N/A")) + ")",
            "  Parent    : " + str(sec.get("parent", "racine")),
            "-" * 70,
        ]
        for p in pts_sec:
            lignes.append(
                "  " + str(p["id"]).rjust(4) + ".  [" +
                p["type"].ljust(15) + "]  " +
                p["nom"].ljust(50) + "  (ligne " + str(p["ligne"]) + ")"
            )
    lignes += ["", "=" * 80, "  CONCORDANCES C1 / C2 / C3", "=" * 80]
    for c in concordances:
        lignes += [
            "",
            "  " + c["code"] + " : " + c["section_source"] +
            " --[" + c["type_relation"] + "]--> " + c["section_cible"],
            "  " + c["description"],
            "  Lemmes HOL : " + c["hol_lemmes"],
        ]
    lignes.append("\n  TOTAL : " + str(len(points)) + " points HOL extraits.")
    return "\n".join(lignes)

# =========================================================================
# PROGRAMME PRINCIPAL
# =========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  PIPELINE HOL - Extraction + SQLite")
    print("  methode_spectral.thy  ->  methode_spectral_hol.db")
    print("=" * 60)

    print("\n[1/5] Lecture de : " + THY_FILE)
    with open(THY_FILE, "r", encoding="utf-8") as f:
        thy_text = f.read()
    print("      OK - " + str(len(thy_text.splitlines())) + " lignes lues.")

    print("\n[2/5] Extraction des points HOL ...")
    points = extraire_points(thy_text)
    print("      OK - " + str(len(points)) + " points extraits.")

    print("\n[3/5] Construction des relations ...")
    relations = construire_relations(points)
    print("      OK - " + str(len(relations)) + " relations construites.")

    print("\n[4/5] Injection SQLite : " + DB_FILE)
    creer_base_sqlite(DB_FILE, SECTIONS_ARCHITECTURE, points, relations, CONCORDANCES)
    print("      OK - Base SQLite creee.")

    print("\n[5/5] Rapport texte : " + TXT_FILE)
    rapport = generer_rapport_texte(points, SECTIONS_ARCHITECTURE, CONCORDANCES)
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write(rapport)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "sections": SECTIONS_ARCHITECTURE,
            "points": points,
            "relations": relations,
            "concordances": CONCORDANCES,
        }, f, indent=2, ensure_ascii=False)
    print("      OK - JSON : " + JSON_FILE)

    print("\n" + "=" * 60)
    print("  SUCCES - Rapport :")
    print("=" * 60)
    print(rapport)
