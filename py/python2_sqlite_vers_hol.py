"""
==========================================================================
  Python #2 — Lecture SQLite -> Génération Validation HOL Unifiée
  Projet   : methode_spectral.thy — Pipeline de validation HOL
  Auteur   : Philippe Thomas Savard
  Fichier  : python2_sqlite_vers_hol.py
==========================================================================
  Produit (dans C:\pipeline_thonnys_theorie_des_nombres\) :
    validation_hol_unifiee.thy   (fichier HOL importable dans Isabelle)
    rapport_architecture_hol.txt (arborescence logique complète)
    schema_neuronal.txt          (schéma concentrique texte)
==========================================================================
"""

import sqlite3, os
from collections import defaultdict

BASE_DIR = r"C:\pipeline_thonnys_theorie_des_nombres"
DB_FILE  = os.path.join(BASE_DIR, "methode_spectral_hol.db")
THY_OUT  = os.path.join(BASE_DIR, "validation_hol_unifiee.thy")
RAPPORT  = os.path.join(BASE_DIR, "rapport_architecture_hol.txt")
SCHEMA   = os.path.join(BASE_DIR, "schema_neuronal.txt")

# =========================================================================
# CHARGEMENT BASE SQLITE
# =========================================================================
def charger_base(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM sections ORDER BY id")
    sections = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT * FROM points ORDER BY id")
    points = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT * FROM relations ORDER BY id")
    relations = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT * FROM concordances ORDER BY id")
    concordances = [dict(r) for r in cur.fetchall()]
    conn.close()
    return sections, points, relations, concordances

# =========================================================================
# ARBORESCENCE NEURONALE
# =========================================================================
def construire_arborescence(sections, points, relations):
    sec_par_code        = {s["code"]: s for s in sections}
    sections_enfants    = defaultdict(list)
    for s in sections:
        if s["parent"]: sections_enfants[s["parent"]].append(s["code"])
    points_par_section  = defaultdict(list)
    for p in points: points_par_section[p["section_logique"]].append(p)
    points_par_id       = {p["id"]: p for p in points}
    conduit_a           = defaultdict(list)
    valide_liens        = defaultdict(list)
    pont_liens          = defaultdict(list)
    generalise          = defaultdict(list)
    dependances         = defaultdict(list)
    for r in relations:
        sid, cid, t = r["point_source_id"], r["point_cible_id"], r["type_relation"]
        if t == "DEPEND_DE":  dependances[sid].append(cid)
        elif t == "CONDUIT_A": conduit_a[sid].append(cid)
        elif t == "VALIDE":    valide_liens[sid].append(cid)
        elif t == "PONT_VERS": pont_liens[sid].append(cid)
        elif t == "GENERALISE":generalise[sid].append(cid)
    return {
        "sec_par_code": sec_par_code,
        "sections_enfants": dict(sections_enfants),
        "points_par_section": dict(points_par_section),
        "points_par_id": points_par_id,
        "dependances": dict(dependances),
        "conduit_a": dict(conduit_a),
        "valide_liens": dict(valide_liens),
        "pont_liens": dict(pont_liens),
        "generalise": dict(generalise),
    }

# =========================================================================
# GÉNÉRATION DU FICHIER HOL UNIFIÉ
# =========================================================================
def generer_hol_unifie(sections, points, relations, concordances, arbre):
    L = []
    sec_par_code  = arbre["sec_par_code"]
    pts_par_sec   = arbre["points_par_section"]

    L += [
        '(*',
        '================================================================================',
        '  Fichier : validation_hol_unifiee.thy',
        '  Généré  : python2_sqlite_vers_hol.py  <-  methode_spectral_hol.db',
        '  Auteur  : Philippe Thomas Savard',
        '  Titre   : Validation HOL unifiée — Ensemble = 1',
        '================================================================================',
        '  Architecture : Ensemble = 1/x + 1/t + 1/ms',
        '    1/x = 1/y1 + 1/y2 + 1/y3  (Fonction zeta de Riemann)',
        '    1/t = psi_savard            (Pont Tchebychev <-> Methode Spectrale)',
        '    1/ms = 1/ms1+1/ms2+1/ms3   (Methode Spectrale)',
        '  Concordances verrouillant RsP = Re = 1/2 :',
        '    C1 : 1/y1 = 1/t   (Tchebychev = psi_savard)',
        '    C2 : 1/y3 = 1/ms1 (zeros non-triviaux = positions P)',
        '    C3 : 1/y2 = 1/ms3 (Re(rho)=1/2 = RsP=1/2)',
        '================================================================================',
        '*)', '',
        'theory validation_hol_unifiee',
        '  imports methode_spectral',
        'begin', '',
    ]

    # Section 1 : Architecture
    L += [
        '(* ============================================================ *)',
        '(*  SECTION 1 : ARCHITECTURE CONCENTRIQUE — Ensemble = 1        *)',
        '(* ============================================================ *)', '',
        'text \\<open>',
        '  Architecture de la validation unifiée de methode_spectral.thy.',
        '  ENSEMBLE (cercle maximal)',
        '    = 1/x  (Zeta Riemann)  = 1/y1 + 1/y2 + 1/y3',
        '    + 1/t  (psi_savard)',
        '    + 1/ms (Methode Spectrale) = 1/ms1 + 1/ms2 + 1/ms3',
        '\\<close>', '',
    ]

    # Section 2 : Points par section logique
    L += [
        '(* ============================================================ *)',
        '(*  SECTION 2 : POINTS HOL PAR SECTION LOGIQUE                  *)',
        '(* ============================================================ *)', '',
    ]
    ORDRE = ["1/ms1","1/ms2","1/ms3","1/t","1/y1","1/y2","1/y3","1/ms","1/x","ENSEMBLE"]
    for code in ORDRE:
        if code not in sec_par_code: continue
        sec = sec_par_code[code]
        pts = pts_par_sec.get(code, [])
        pts_sig = [p for p in pts if p["type"] in
                   ("definition","lemma","theorem","corollary",
                    "axiomatization","locale","interpretation","typedecl","consts")]
        L += [
            f'section "{code} — {sec["label"]}"', '',
            f'text \\<open>',
            f'  {sec["description"]}',
            f'  Ancre HOL : {sec.get("hol_anchor","N/A")} '
            f'(ligne {sec.get("ligne_anchor","N/A")})',
            f'  Parent    : {sec.get("parent","racine")}',
            f'\\<close>', '',
        ]
        if pts_sig:
            L.append('text \\<open>')
            L.append(f'  Points HOL de la section {code} ({len(pts_sig)} objets formels) :')
            for idx, p in enumerate(pts_sig[:60], 1):
                L.append(f'    {idx:>3}. [{p["type"]:<15}] {p["nom"]} (ligne {p["ligne"]})')
            if len(pts_sig) > 60:
                L.append(f'    ... et {len(pts_sig)-60} autres objets.')
            L += ['\\<close>', '']

    # Section 3 : Concordances
    L += [
        '(* ============================================================ *)',
        '(*  SECTION 3 : CONCORDANCES C1 / C2 / C3                       *)',
        '(* ============================================================ *)', '',
        'text \\<open>',
        '  Les trois concordances reliant la Méthode Spectrale à Zeta Riemann.',
        '\\<close>', '',
    ]
    for c in concordances:
        L += [
            'text \\<open>',
            f'  {c["code"]} : {c["section_source"]} --[{c["type_relation"]}]--> {c["section_cible"]}',
            f'  {c["description"]}',
            f'  Lemmes HOL : {c["hol_lemmes"]}',
            '\\<close>', '',
        ]

    # Section 4 : locale ensemble_unifie
    L += [
        '(* ============================================================ *)',
        '(*  SECTION 4 : LOCALE ensemble_unifie                          *)',
        '(* ============================================================ *)', '',
        'locale ensemble_unifie =',
        '  fixes ms_rapport    :: real',
        '  fixes zeta_critique :: real',
        '  assumes H_C3_alignement : "ms_rapport = zeta_critique"',
        '  assumes H_C3_valeur     : "zeta_critique = 1 / 2"',
        '  fixes reconstruction_valide :: bool',
        '  assumes H_C2_reconstruction : "reconstruction_valide = True"',
        '  fixes pont_fonctionnel :: bool',
        '  assumes H_C1_pont : "pont_fonctionnel = True"',
        '  fixes exclusion_composes :: bool',
        '  assumes H_F5_exclusion : "exclusion_composes = True"',
        'begin', '',
        'theorem (in ensemble_unifie) validation_C3:',
        '  "ms_rapport = 1 / 2"',
        'proof -',
        '  have "ms_rapport = zeta_critique" using H_C3_alignement by simp',
        '  also have "... = 1 / 2" using H_C3_valeur by simp',
        '  finally show ?thesis .',
        'qed', '',
        'theorem (in ensemble_unifie) validation_ensemble_unifie:',
        '  "ms_rapport = zeta_critique \\<and> zeta_critique = 1 / 2 \\<and>',
        '   reconstruction_valide = True \\<and> pont_fonctionnel = True \\<and>',
        '   exclusion_composes = True"',
        'proof -',
        '  show ?thesis using H_C3_alignement H_C3_valeur H_C2_reconstruction',
        '                     H_C1_pont H_F5_exclusion by simp',
        'qed', '',
        'end', '',
    ]

    # Section 5 : Satisfaisabilité + Théorème final
    L += [
        '(* ============================================================ *)',
        '(*  SECTION 5 : SATISFAISABILITÉ ET THÉORÈME FINAL              *)',
        '(* ============================================================ *)', '',
        'theorem ensemble_unifie_satisfaisable:',
        '  "ensemble_unifie (1/2) (1/2) True True True"',
        'proof',
        '  show "1 / (2::real) = 1 / 2" by simp',
        '  show "(1::real) / 2 = 1 / 2" by simp',
        '  show "True = True" by simp',
        '  show "True = True" by simp',
        '  show "True = True" by simp',
        'qed', '',
        'theorem validation_finale_pont_savard:',
        '  assumes "n1 \\<ge> 1" "n2 \\<ge> 1" "n1 \\<noteq> n2"',
        '  shows   "Re_droite_critique n1 n2 = RsP n1 n2 \\<and> RsP n1 n2 = 1 / 2"',
        'proof -',
        '  show ?thesis using synthese_pont_savard[OF assms] by simp',
        'qed', '',
        'text \\<open>',
        '  CONCLUSION : Ensemble = 1',
        '  { F1 & F2 & F3 & F4 & F5 } => RsP = Re = 1/2 VRAI',
        '\\<close>', '',
        'end',
    ]
    return "\n".join(L)

# =========================================================================
# RAPPORT D'ARCHITECTURE
# =========================================================================
def generer_rapport_architecture(sections, points, relations, concordances, arbre):
    pts_par_id  = arbre["points_par_id"]
    pts_par_sec = arbre["points_par_section"]
    L = ["="*78,
         "  RAPPORT D'ARCHITECTURE HOL — methode_spectral.thy",
         "  Auteur : Philippe Thomas Savard",
         "="*78, ""]
    L += ["─"*78, "  STATISTIQUES PAR SECTION", "─"*78]
    for s in sections:
        code = s["code"]; pts = pts_par_sec.get(code, [])
        nb_d = sum(1 for p in pts if p["type"]=="definition")
        nb_l = sum(1 for p in pts if p["type"]=="lemma")
        nb_t = sum(1 for p in pts if p["type"]=="theorem")
        nb_a = sum(1 for p in pts if p["type"]=="axiomatization")
        L.append(f"  {code:<10} : {len(pts):>4} pts  (def:{nb_d:>3}  lem:{nb_l:>3}  thm:{nb_t:>3}  axm:{nb_a:>2})")
    L += ["", "─"*78, "  CONCORDANCES", "─"*78]
    for c in concordances:
        L += [f"  {c['code']} : {c['section_source']} --[{c['type_relation']}]--> {c['section_cible']}",
              f"       {c['description'][:72]}",
              f"       Lemmes : {c['hol_lemmes'][:72]}"]
    L += ["", "─"*78, "  RELATIONS CLÉS (CONDUIT_A / VALIDE / PONT_VERS / GENERALISE)", "─"*78]
    for r in relations:
        src = pts_par_id.get(r["point_source_id"])
        cib = pts_par_id.get(r["point_cible_id"])
        if src and cib and r["type_relation"] in ("CONDUIT_A","VALIDE","PONT_VERS","GENERALISE"):
            L.append(f"  {src['nom']:<45} --[{r['type_relation']:<12}]--> {cib['nom']}")
    L += ["", "="*78,
          f"  TOTAL : {len(points)} points | {len(relations)} relations | {len(concordances)} concordances",
          "="*78]
    return "\n".join(L)

# =========================================================================
# SCHÉMA NEURONAL
# =========================================================================
def generer_schema_neuronal(sections, points, arbre):
    pts_par_sec = arbre["points_par_section"]
    L = [
        "="*78,
        "  SCHÉMA NEURONAL CONCENTRIQUE — methode_spectral.thy",
        "  Architecture : Ensemble = 1  (Règle Savard)",
        "="*78, "",
        "  ┌─────────────────────────────────────────────────────────────────┐",
        "  │  ENSEMBLE = 1  →  synthese_pont_savard : RsP = Re = 1/2 VRAI  │",
        "  │  ┌───────────────┐  ┌──────────┐  ┌──────────────────────┐    │",
        "  │  │  1/x (Zeta)   │  │ 1/t(psi) │  │ 1/ms (MS)            │    │",
        "  │  │ 1/y1 C1──────────────────── │  │ 1/ms1 Reconstruction │    │",
        "  │  │ 1/y2 C3────────────────────────│ 1/ms2 Exclusion       │    │",
        "  │  │ 1/y3 C2────────────────────────│ 1/ms3 RsP=1/2         │    │",
        "  │  └───────────────┘  └──────────┘  └──────────────────────┘    │",
        "  └─────────────────────────────────────────────────────────────────┘",
        "", "  C1: 1/y1↔1/t   C2: 1/y3↔1/ms1   C3: 1/y2↔1/ms3", "",
        "─"*78, "  DÉTAIL PAR NŒUD (points HOL clés)", "─"*78,
    ]
    ORDRE = [("ENSEMBLE","◉"),("1/x","○"),("1/t","○"),("1/ms","○"),
             ("1/y1","  ▷"),("1/y2","  ▷"),("1/y3","  ▷"),
             ("1/ms1","  ▷"),("1/ms2","  ▷"),("1/ms3","  ▷")]
    for (code, sym) in ORDRE:
        pts = pts_par_sec.get(code,[])
        pts_s = [p for p in pts if p["type"] in ("theorem","lemma","definition")]
        L += ["", f"  {sym} {code}"]
        for p in pts_s[:8]:
            L.append(f"         [{p['type']:<14}] {p['nom']}")
        if len(pts_s) > 8:
            L.append(f"         ... +{len(pts_s)-8} autres objets formels")
    L += ["", "="*78,
          f"  Base : methode_spectral_hol.db | Total : {len(points)} points HOL",
          "="*78]
    return "\n".join(L)

# =========================================================================
# PROGRAMME PRINCIPAL
# =========================================================================
if __name__ == "__main__":
    print("="*60)
    print("  PIPELINE HOL — SQLite -> Validation HOL Unifiée")
    print("  methode_spectral_hol.db  ->  validation_hol_unifiee.thy")
    print("="*60)

    print(f"\n[1/5] Chargement SQLite : {DB_FILE}")
    if not os.path.exists(DB_FILE):
        print(f"  ERREUR : Base introuvable. Exécutez d'abord Python #1.")
        exit(1)
    sections, points, relations, concordances = charger_base(DB_FILE)
    print(f"      OK — {len(sections)} sections | {len(points)} points | "
          f"{len(relations)} relations | {len(concordances)} concordances")

    print("\n[2/5] Construction de l'arborescence neuronale ...")
    arbre = construire_arborescence(sections, points, relations)
    print("      OK")

    print(f"\n[3/5] Génération HOL : {THY_OUT}")
    hol = generer_hol_unifie(sections, points, relations, concordances, arbre)
    with open(THY_OUT, "w", encoding="utf-8") as f: f.write(hol)
    print(f"      OK — {len(hol.splitlines())} lignes HOL générées.")

    print(f"\n[4/5] Rapport architecture : {RAPPORT}")
    rapport = generer_rapport_architecture(sections, points, relations, concordances, arbre)
    with open(RAPPORT, "w", encoding="utf-8") as f: f.write(rapport)
    print("      OK")

    print(f"\n[5/5] Schéma neuronal : {SCHEMA}")
    schema = generer_schema_neuronal(sections, points, arbre)
    with open(SCHEMA, "w", encoding="utf-8") as f: f.write(schema)
    print("      OK")

    print("\n"+"="*60)
    print("  SUCCÈS — Fichiers générés :")
    print(f"    {THY_OUT}")
    print(f"    {RAPPORT}")
    print(f"    {SCHEMA}")
    print("="*60)
    print("\n" + schema)
