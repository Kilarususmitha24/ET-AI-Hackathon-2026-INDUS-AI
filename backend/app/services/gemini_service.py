import json
import re
from typing import Optional

import google.generativeai as genai

from app.config import get_settings

settings = get_settings()


class GeminiService:
    def __init__(self):
        self._configured = False
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
            self._configured = True
            self.model = genai.GenerativeModel(settings.gemini_model)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not self._configured:
            return self._mock_embeddings(texts)
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=settings.embedding_model,
                content=text,
                task_type="retrieval_document",
            )
            embeddings.append(result["embedding"])
        return embeddings

    def _mock_embeddings(self, texts: list[str]) -> list[list[float]]:
        import hashlib
        import struct

        embeddings = []
        for text in texts:
            h = hashlib.sha256(text.encode()).digest()
            vec = []
            for i in range(0, min(len(h), 96), 4):
                val = struct.unpack("f", h[i : i + 4])[0] if i + 4 <= len(h) else 0.1
                vec.append(val)
            while len(vec) < 768:
                vec.extend(vec[: min(768 - len(vec), len(vec))])
            embeddings.append(vec[:768])
        return embeddings

    def generate(self, prompt: str, system: str = "") -> str:
        if not self._configured:
            return self._mock_response(prompt)
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        response = self.model.generate_content(full_prompt)
        return response.text or "No response generated."

    def _mock_response(self, prompt: str) -> str:
        if "root cause" in prompt.lower() or "incident" in prompt.lower():
            return json.dumps({
                "probable_causes": [
                    "Bearing wear due to insufficient lubrication",
                    "Misalignment from recent maintenance",
                    "Contamination in hydraulic fluid",
                ],
                "contributing_factors": [
                    "Extended operating hours beyond schedule",
                    "Delayed preventive maintenance",
                    "Ambient temperature exceeding design limits",
                ],
                "recommended_actions": [
                    "Inspect bearing assembly and replace if worn",
                    "Perform laser alignment check",
                    "Flush and replace hydraulic fluid",
                    "Update maintenance schedule in CMMS",
                ],
                "analysis_summary": "Based on symptom patterns and historical incident data, mechanical wear combined with maintenance gaps is the most likely root cause.",
            })
        return (
            "Based on the retrieved industrial knowledge base, I recommend reviewing the "
            "relevant maintenance procedures and safety manuals. Configure GEMINI_API_KEY "
            "for full AI-powered responses with document-grounded analysis."
        )

    def extract_entities(self, text: str) -> dict:
        prompt = f"""Extract industrial entities from this text. Return ONLY valid JSON with keys:
equipment (list), procedures (list), incidents (list), regulations (list), locations (list).

Text:
{text[:4000]}"""

        response = self.generate(prompt, "You are an industrial knowledge extraction AI. Return only JSON.")
        try:
            match = re.search(r"\{.*\}", response, re.DOTALL)
            if match:
                return json.loads(match.group())
        except json.JSONDecodeError:
            pass
        return self._regex_extract(text)

    def _regex_extract(self, text: str) -> dict:
        equipment_keywords = ["pump", "compressor", "turbine", "valve", "motor", "boiler", "reactor", "conveyor"]
        regulation_keywords = ["OSHA", "ISO", "EPA", "API", "ASME", "NFPA", "IEC"]
        found_equipment = list({kw.title() for kw in equipment_keywords if kw.lower() in text.lower()})
        found_regs = list({kw for kw in regulation_keywords if kw in text})
        return {
            "equipment": found_equipment or ["Industrial Equipment"],
            "procedures": ["Standard Operating Procedure"],
            "incidents": [],
            "regulations": found_regs or ["ISO 45001"],
            "locations": ["Plant Floor"],
        }
