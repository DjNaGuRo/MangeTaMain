"""
Constantes pour l'analyse de sentiment et le preprocessing
"""

import re

# === LEXIQUES DE SENTIMENT ===
NEGATION_WORDS = {
    "no",
    "not",
    "nor",
    "never",
    "neither",
    "none",
    "nobody",
    "nothing",
    "nowhere",
    "hardly",
    "barely",
    "scarcely",
    "rarely",
    "seldom",
    "without",
    "cannot",
    "can't",
    "won't",
    "wouldn't",
    "shouldn't",
    "didn't",
    "doesn't",
    "don't",
    "isn't",
    "aren't",
    "wasn't",
    "weren't",
}

POSITIVE_WORDS = {
    "good",
    "great",
    "excellent",
    "amazing",
    "wonderful",
    "perfect",
    "love",
    "like",
    "recommend",
    "delicious",
    "tasty",
    "tender",
    "juicy",
    "crispy",
    "easy",
    "quick",
}

NEGATIVE_WORDS = {
    "bad",
    "bland",
    "dry",
    "tough",
    "rubbery",
    "chewy",
    "soggy",
    "salty",
    "bitter",
    "sour",
    "greasy",
    "oily",
    "burnt",
    "overcooked",
    "undercooked",
    "gross",
    "disgusting",
    "horrible",
    "terrible",
    "inedible",
    "stale",
    "watery",
    "runny",
    "thick",
    "thin",
    "hard",
    "raw",
    "uncooked",
    "boring",
    "awkward",
    "messy",
    "confusing",
    "complicated",
}

# === CONTRACTIONS ===
CONTRACTIONS = {
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "can't": "cannot",
    "won't": "will not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "shouldn't": "should not",
    "wouldn't": "would not",
    "couldn't": "could not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "ain't": "is not",
}

# === PATTERNS REGEX ===
SUBTLE_NEG_PATTERN = (
    r"(just ok(?:ay)?|not really|didn't really|misleading|disappointed|expected better|"
    r"could be better|nothing special|mediocre|average at best|wouldn't recommend|"
    r"not impressed|fell short|lacked flavor|lack of|underwhelming|under season(?:ed)?|"
    r"over season(?:ed)?|too (?:salty|sweet|spicy|greasy|oily|dry|thick|thin)|"
    r"burnt|overcooked|undercooked)"
)

NEGATED_POS_PATTERN = (
    r"^(?:not_(?:good|great|excellent|amazing|wonderful|perfect|love|like|recommend|delicious|tasty)|"
    r"(?:good|great|excellent|amazing|wonderful|perfect|love|like|recommend|delicious|tasty)_NEG)$"
)

# === REGEX COMPILÉS ===
SUBTLE_NEG_RE = re.compile(SUBTLE_NEG_PATTERN, re.IGNORECASE)
NEGATED_POS_RE = re.compile(NEGATED_POS_PATTERN)
CONTRACTIONS_RE = re.compile(
    r"\b(" + "|".join(map(re.escape, CONTRACTIONS)) + r")\b", re.IGNORECASE
)
TOKEN_RE = re.compile(r"[A-Za-z']+|[.!?;]")
SENTENCE_SPLIT_RE = re.compile(r"[.!?;]+")

# === AUTRES CONSTANTES ===
CLAUSE_BREAKERS = {".", "!", "?", ";", "but", "however", "though", "although", "yet"}
DEFAULT_NEGATION_WINDOW = 3

# === SEUILS NUTRITIONNELS ===
NUTRITION_THRESHOLDS = {
    "calories": 3000,
    "sodium": 5000,
    "protein": 500,
    "sugar": 500,
    "max_cooking_minutes": 43200,  # 1 mois
}
