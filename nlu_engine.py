"""
=============================================================================
TECNOLÓGICO NACIONAL DE MÉXICO - INSTITUTO TECNOLÓGICO SUPERIOR DE URUAPAN
DIVISIÓN DE ESTUDIOS DE POSGRADO E INVESTIGACIÓN
MAESTRÍA EN INTELIGENCIA ARTIFICIAL

Materia: Inteligencia Artificial y su Ética
Actividad 17: PLN - Chatbot de Atención al Cliente (NLU Engine)
Alumno: Juan Pablo Figueroa Moran (Matrícula: M26040059)
=============================================================================
"""

import sys
import json
import re
import os
import random
import numpy as np
from typing import Tuple, Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ChatbotNLU:
    """
    Motor NLU híbrido:
    1. Pre-filtro con expresiones regulares deterministas.
    2. Clasificador semántico basado en matriz TF-IDF y similitud cosenoidal.
    3. Lógica de fallback cuando la confianza máxima es inferior al 60% (0.60).
    """
    FALLBACK_THRESHOLD = 0.60

    def __init__(self, intents_path: str = "intents.json"):
        self.intents_path = intents_path
        self.intents_data: Dict[str, Any] = {}
        self.patterns_list: List[str] = []
        self.tags_list: List[str] = []
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
        self.tfidf_matrix = None
        self.regex_rules: Dict[str, List[re.Pattern]] = {}
        
        self._cargar_intenciones()
        self._compilar_regex()
        self._entrenar_tfidf()

    def _cargar_intenciones(self):
        if not os.path.exists(self.intents_path):
            # Intentar ruta relativa
            alt_path = os.path.join(os.path.dirname(__file__), "intents.json")
            if os.path.exists(alt_path):
                self.intents_path = alt_path
            else:
                raise FileNotFoundError(f"No se encontró el archivo de intenciones: {self.intents_path}")

        with open(self.intents_path, "r", encoding="utf-8") as f:
            self.intents_data = json.load(f)

    def _compilar_regex(self):
        """Compila patrones regex para coincidencias directas y de alta prioridad."""
        for intent in self.intents_data.get("intents", []):
            tag = intent["tag"]
            patterns = intent["patterns"]
            compiled = []
            for p in patterns:
                # Regex flexible con límites de palabra
                escaped = re.escape(p).replace(r"\ ", r"\s+")
                pattern_re = re.compile(rf"\b{escaped}\b", re.IGNORECASE)
                compiled.append(pattern_re)
            self.regex_rules[tag] = compiled

    def _entrenar_tfidf(self):
        """Vectoriza los patrones de entrenamiento con TF-IDF."""
        self.patterns_list = []
        self.tags_list = []
        for intent in self.intents_data.get("intents", []):
            tag = intent["tag"]
            for pat in intent["patterns"]:
                self.patterns_list.append(pat)
                self.tags_list.append(tag)

        self.tfidf_matrix = self.vectorizer.fit_transform(self.patterns_list)

    def clasificar_intencion(self, mensaje_usuario: str) -> Tuple[str, float, str]:
        """
        Retorna (tag_intencion, puntaje_confianza, respuesta_seleccionada).
        """
        texto_limpio = mensaje_usuario.strip()
        if not texto_limpio:
            return "vacio", 1.0, "Por favor escribe tu consulta para poder ayudarte."

        # 1. Matching por Expresiones Regulares
        for tag, compiled_list in self.regex_rules.items():
            for pat in compiled_list:
                if pat.search(texto_limpio):
                    respuesta = self._obtener_respuesta(tag)
                    return tag, 0.95, respuesta

        # 2. Similitud Cosenoidal TF-IDF
        vec_usuario = self.vectorizer.transform([texto_limpio])
        similitudes = cosine_similarity(vec_usuario, self.tfidf_matrix)[0]
        
        idx_max = int(np.argmax(similitudes))
        confianza_max = float(similitudes[idx_max])
        tag_predicho = self.tags_list[idx_max]

        # 3. Lógica de Fallback (< 60%)
        if confianza_max < self.FALLBACK_THRESHOLD:
            respuesta_fallback = (
                f"Disculpa, mi nivel de certidumbre es bajo ({confianza_max*100:.1f}%). "
                "No logro comprender con precisión tu solicitud. ¿Podrías reformular tu consulta "
                "o escribir 'contacto humano' para transferirte con un asesor?"
            )
            return "fallback", confianza_max, respuesta_fallback

        respuesta = self._obtener_respuesta(tag_predicho)
        return tag_predicho, confianza_max, respuesta

    def _obtener_respuesta(self, tag: str) -> str:
        for intent in self.intents_data.get("intents", []):
            if intent["tag"] == tag:
                return random.choice(intent["responses"])
        return "Gracias por contactarnos. ¿Hay algo más en lo que pueda apoyarte?"
