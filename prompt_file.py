# =============================================================================
# prompt_file.py
# HireBox Data — Fichier de prompts pour la génération de questions d'entretien
# Modèle : zai-org/GLM-5.1
# =============================================================================
#
# Ce fichier centralise tous les prompts utilisés dans le pipeline HireBox.
# Il définit le system prompt, le user prompt template, ainsi que des utilitaires
# pour construire les messages à envoyer au modèle GLM-5.1.
#
# Usage :
#   from prompt_file import build_messages
#   messages = build_messages(cv_text="...")
# =============================================================================


# -----------------------------------------------------------------------------
# SYSTEM PROMPT
# Définit le rôle et le comportement du modèle.
# -----------------------------------------------------------------------------

SYSTEM_PROMPT = """Tu es un expert en recrutement et en entretiens professionnels.
Tu as pour mission d'analyser le contenu d'un CV de candidat et de formuler \
une question d'entretien pertinente, ciblée et ouverte, basée sur un élément \
spécifique du parcours du candidat.

Règles impératives :
- Lis attentivement l'intégralité du CV fourni.
- Sélectionne UN SEUL élément saillant parmi : une expérience professionnelle, \
un projet, une compétence technique, une formation ou une réalisation notable.
- Formule UNE SEULE question, ouverte et précise, qui invite le candidat à \
approfondir cet élément.
- La question doit être naturelle, bienveillante et propice à l'échange.
- Ne liste pas plusieurs questions. Ne fais pas de commentaires sur le CV. \
Ne te présente pas.
- Réponds uniquement avec la question, sans introduction ni conclusion."""


# -----------------------------------------------------------------------------
# USER PROMPT TEMPLATE
# Template principal à utiliser pour chaque CV soumis.
# Le paramètre {cv_text} sera remplacé par le contenu brut du CV.
# -----------------------------------------------------------------------------

USER_PROMPT_TEMPLATE = """Voici le CV du candidat :

---
{cv_text}
---

Sur la base de ce CV, génère une question d'entretien pertinente et ouverte \
portant sur un élément spécifique du parcours de ce candidat."""


# -----------------------------------------------------------------------------
# VARIANTES DE PROMPTS
# Permettent d'ajuster le comportement selon le contexte (langue, ton, niveau).
# -----------------------------------------------------------------------------

# Variante : question en anglais
USER_PROMPT_TEMPLATE_EN = """Here is the candidate's resume:

---
{cv_text}
---

Based on this resume, generate one relevant and open-ended interview question \
focused on a specific element of this candidate's background."""

SYSTEM_PROMPT_EN = """You are an expert recruiter and interview specialist.
Your task is to read a candidate's resume and generate one targeted, open-ended \
interview question based on a specific and noteworthy element of their background.

Rules:
- Read the entire resume carefully.
- Select ONE element: a work experience, project, technical skill, education, or achievement.
- Generate ONE open-ended question that invites the candidate to elaborate.
- The question must be natural, professional, and conversational.
- Do not list multiple questions. Do not comment on the resume. Do not introduce yourself.
- Reply with the question only, no preamble or conclusion."""


# Variante : ton plus formel (entretiens de direction / poste senior)
SYSTEM_PROMPT_SENIOR = """Tu es un directeur des ressources humaines expérimenté, \
spécialisé dans le recrutement de profils seniors et de cadres dirigeants.
Analyse le CV fourni et formule une question d'entretien approfondie, \
stratégique et exigeante, portant sur un aspect clé du leadership, \
de la vision ou des réalisations à fort impact du candidat.

Règles :
- Sélectionne un élément à forte valeur ajoutée (direction d'équipe, \
transformation organisationnelle, résultats mesurables, prise de décision stratégique).
- Formule UNE SEULE question, rigoureuse et ouverte, qui teste la profondeur \
de réflexion du candidat.
- Ne fais aucun commentaire. Réponds uniquement avec la question."""


# Variante : profil junior / stage
SYSTEM_PROMPT_JUNIOR = """Tu es un recruteur bienveillant spécialisé dans l'accueil \
de profils juniors, stagiaires et jeunes diplômés.
Analyse le CV fourni et formule une question d'entretien encourageante et accessible, \
qui met en valeur le potentiel, la motivation ou les premières expériences du candidat.

Règles :
- Sélectionne un élément positif : un projet académique, un stage, \
une activité extra-curriculaire, une compétence acquise ou une initiative personnelle.
- Formule UNE SEULE question, ouverte et bienveillante, qui invite le candidat \
à parler de son parcours avec enthousiasme.
- Ne fais aucun commentaire. Réponds uniquement avec la question."""


# -----------------------------------------------------------------------------
# CONSTANTES DE CONFIGURATION DU MODÈLE
# Paramètres recommandés pour GLM-5.1 dans ce cas d'usage.
# -----------------------------------------------------------------------------

MODEL_ID = "zai-org/GLM-5.1"

# Paramètres de génération recommandés
GENERATION_CONFIG = {
    "max_new_tokens": 150,       # Une question ne dépasse pas 150 tokens
    "temperature": 0.8,          # Légère créativité pour varier les questions
    "top_p": 0.92,               # Nucleus sampling équilibré
    "do_sample": True,
    "repetition_penalty": 1.1,   # Évite les répétitions dans la formulation
}

# Longueur maximale du CV en tokens (au-delà, le texte sera tronqué)
MAX_CV_TOKENS = 3000


# -----------------------------------------------------------------------------
# FONCTIONS UTILITAIRES
# Construisent les messages prêts à être envoyés au modèle.
# -----------------------------------------------------------------------------

def build_messages(
    cv_text: str,
    language: str = "fr",
    level: str = "standard"
) -> list[dict]:
    """
    Construit la liste de messages (format chat) à envoyer à GLM-5.1.

    Args:
        cv_text  : Texte brut extrait du CV du candidat.
        language : Langue de la question générée. "fr" (défaut) ou "en".
        level    : Niveau du poste visé. "standard" (défaut), "senior", "junior".

    Returns:
        Liste de messages au format [{"role": ..., "content": ...}].

    Example:
        >>> messages = build_messages(cv_text="Jean Dupont, 5 ans d'exp...")
        >>> # Envoyer messages au modèle via pipeline ou API
    """
    # Sélection du system prompt
    if language == "en":
        system = SYSTEM_PROMPT_EN
        user_template = USER_PROMPT_TEMPLATE_EN
    elif level == "senior":
        system = SYSTEM_PROMPT_SENIOR
        user_template = USER_PROMPT_TEMPLATE
    elif level == "junior":
        system = SYSTEM_PROMPT_JUNIOR
        user_template = USER_PROMPT_TEMPLATE
    else:
        system = SYSTEM_PROMPT
        user_template = USER_PROMPT_TEMPLATE

    # Nettoyage et troncature légère du CV si nécessaire
    cv_cleaned = _clean_cv_text(cv_text)

    user_content = user_template.format(cv_text=cv_cleaned)

    return [
        {"role": "system", "content": system},
        {"role": "user",   "content": user_content},
    ]


def build_messages_raw(cv_text: str) -> list[dict]:
    """
    Version simplifiée : construit les messages avec les paramètres par défaut.
    Équivalent à build_messages(cv_text, language="fr", level="standard").

    Args:
        cv_text : Texte brut du CV.

    Returns:
        Liste de messages prêts à être soumis au modèle.
    """
    return build_messages(cv_text=cv_text)


def _clean_cv_text(cv_text: str, max_chars: int = 12000) -> str:
    """
    Nettoie et tronque le texte du CV pour s'assurer qu'il reste
    dans les limites du contexte du modèle.

    Args:
        cv_text  : Texte brut du CV.
        max_chars: Nombre maximum de caractères autorisé (défaut : 12 000).

    Returns:
        Texte nettoyé et potentiellement tronqué.
    """
    # Suppression des espaces excessifs et lignes vides multiples
    lines = [line.strip() for line in cv_text.splitlines()]
    cleaned_lines = []
    prev_empty = False
    for line in lines:
        if line == "":
            if not prev_empty:
                cleaned_lines.append(line)
            prev_empty = True
        else:
            cleaned_lines.append(line)
            prev_empty = False

    cleaned = "\n".join(cleaned_lines).strip()

    # Troncature si le CV est trop long
    if len(cleaned) > max_chars:
        cleaned = cleaned[:max_chars] + "\n[...CV tronqué pour respecter la limite de contexte...]"

    return cleaned


# -----------------------------------------------------------------------------
# EXEMPLES D'UTILISATION
# Démonstration du pipeline complet avec GLM-5.1 via HuggingFace Transformers.
# -----------------------------------------------------------------------------

USAGE_EXAMPLE = '''
# Exemple d'utilisation avec HuggingFace Transformers

from transformers import pipeline
from prompt_file import build_messages, GENERATION_CONFIG, MODEL_ID

# Chargement du pipeline de génération de texte
pipe = pipeline(
    "text-generation",
    model=MODEL_ID,
    device_map="auto",
    torch_dtype="auto",
)

# Texte du CV (extrait)
cv_text = """
Alice Martin
Ingénieure Data Science | 3 ans d\'expérience

EXPÉRIENCES
- Data Scientist, FinTech Innov (2023-2025)
  Développement d\'un modèle de scoring crédit (XGBoost, AUC 0.91)
  Réduction de 30% des faux positifs sur la détection de fraude

- Stage Data Analyst, BankCorp (2022)
  Analyse de données transactionnelles, dashboards Power BI

FORMATION
- Master 2 Data Science, Université Paris-Saclay (2022)
- Licence Mathématiques Appliquées, Sorbonne (2020)

COMPÉTENCES
Python, SQL, Scikit-learn, TensorFlow, Spark, AWS
"""

# Construction des messages
messages = build_messages(cv_text=cv_text, language="fr", level="standard")

# Génération de la question
output = pipe(messages, **GENERATION_CONFIG)
question = output[0]["generated_text"][-1]["content"]

print("Question générée :", question)
# Exemple de sortie :
# "Vous avez réduit de 30% les faux positifs sur la détection de fraude chez
#  FinTech Innov — pouvez-vous me décrire la démarche que vous avez suivie
#  pour atteindre ce résultat ?"
'''
