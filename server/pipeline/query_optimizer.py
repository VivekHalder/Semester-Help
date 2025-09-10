from __future__ import annotations
import re
from typing import List, Dict, Tuple

_STOP = {
    "please","explain","what","is","are","the","a","an","and","or","of","to","in","on","for",
    "with","about","me","give","show","how","why","does","do","did","can","could","should",
    "brief","short","concise","overview","summarize","detail","detailed","comprehensive"
}

_ACRONYMS: Dict[str, List[str]] = {
    "bjt": ["bipolar junction transistor"],
    "fet": ["field effect transistor"],
    "mosfet": ["metal oxide semiconductor field effect transistor"],
    "opamp": ["operational amplifier","op-amp"],
    "op-amp": ["operational amplifier","opamp"],
    "fft": ["fast fourier transform"],
    "dft": ["discrete fourier transform"],
    "psd": ["power spectral density"],
    "lti": ["linear time invariant"],
    "v-i": ["voltage current"],
    "kvl": ["kirchhoff voltage law"],
    "kcl": ["kirchhoff current law"],
    "rms": ["root mean square"],
    "snr": ["signal to noise ratio"],
}

_SYNONYMS: Dict[str, List[str]] = {
    "bandgap": ["forbidden energy gap","energy band gap","Eg"],
    "reactance": ["capacitive reactance","inductive reactance","Xc","Xl"],
    "transfer function": ["H(jω)","frequency response"],
    "cutoff frequency": ["corner frequency","-3 dB frequency","f_c"],
    "biasing": ["dc operating point","Q-point","quiescent point"],
    "small-signal": ["incremental","linearized"],
    "gain": ["amplification","A_v","voltage gain"],
    "impedance": ["Z","equivalent impedance"],
    "admittance": ["Y","inverse impedance"],
    "emf": ["electromotive force"],
    "resonance": ["resonant frequency","ω0","f0"],
}

_INTENT_HINTS = {
    "define": ["definition","describe","what is"],
    "derive": ["derive","derivation","prove","show that"],
    "formula": ["formula","equation","expression"],
    "example": ["example","numerical","problem"],
    "application": ["application","use","practical"],
    "comparison": ["compare","versus","advantage","disadvantage","pros","cons"],
}

_UNIT_NORMALIZERS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\bohms?\b", re.I), "Ω"),
    (re.compile(r"\bmicro\b", re.I), "µ"),
    (re.compile(r"\bmega\b", re.I), "M"),
    (re.compile(r"\bkilo\b", re.I), "k"),
    (re.compile(r"\bdeg(?:ree)?s?\s*c\b", re.I), "°C"),
    (re.compile(r"\bdegrees?\s*f\b", re.I), "°F"),
]

_WORD_RE = re.compile(r"[A-Za-z0-9+_\-./]+")
_WS = re.compile(r"\s+")

def _normalize_units(text: str) -> str:
    t = text
    for pat, repl in _UNIT_NORMALIZERS:
        t = pat.sub(repl, t)
    return t

def _strip_punct(text: str) -> str:
    t = re.sub(r"[^\w+\-./°Ωµ ]+", " ", text)
    return _WS.sub(" ", t).strip()

def _lower(s: str) -> str:
    return s.lower()

def _tokenize(s: str) -> List[str]:
    return [m.group(0) for m in _WORD_RE.finditer(s)]

def _remove_stopwords(tokens: List[str]) -> List[str]:
    return [w for w in tokens if w.lower() not in _STOP and not w.isdigit()]

def _expand_acronyms(tokens: List[str]) -> List[str]:
    out = []
    for w in tokens:
        lw = w.lower()
        out.append(w)
        if lw in _ACRONYMS:
            out.extend(_ACRONYMS[lw])
    return out

def _expand_synonyms(tokens: List[str]) -> List[str]:
    out = []
    for w in tokens:
        out.append(w)
        lw = w.lower()
        if lw in _SYNONYMS:
            out.extend(_SYNONYMS[lw])
    return out

def _extract_intent(question_lc: str) -> List[str]:
    hints = []
    for key, words in _INTENT_HINTS.items():
        if any(w in question_lc for w in words):
            hints.append(key)
    return hints

def _most_recent_topic(chat_history: str) -> List[str]:
    # naive backfill: take last non-empty line’s content words
    lines = [l.strip() for l in chat_history.splitlines() if l.strip()]
    if not lines:
        return []
    tail = lines[-1]
    tail = _normalize_units(_strip_punct(_lower(tail)))
    toks = _remove_stopwords(_tokenize(tail))
    return toks[-10:] if toks else []

def _dedupe_order(seq: List[str]) -> List[str]:
    seen = set()
    out = []
    for x in seq:
        k = x.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(x)
    return out

def _limit_tokens(words: List[str], max_words: int = 40) -> List[str]:
    return words[:max_words]

def optimize_query(question: str, chat_history: str) -> str:
    if not question:
        return ""

    q0 = _normalize_units(_strip_punct(_lower(question)))
    toks = _tokenize(q0)
    toks = _remove_stopwords(toks)

    if len(toks) < 3:
        toks.extend(_most_recent_topic(chat_history))

    toks = _expand_acronyms(toks)
    toks = _expand_synonyms(toks)
    toks = _dedupe_order(toks)
    toks = _limit_tokens(toks, 48)

    intent = _extract_intent(q0)
    if intent:
        toks.extend([f"[{i}]" for i in intent])

    query = " ".join(toks).strip()
    return query if query else question.strip()
