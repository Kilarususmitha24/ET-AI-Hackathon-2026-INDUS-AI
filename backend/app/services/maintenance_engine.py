from datetime import datetime, timedelta

MAINTENANCE_PATTERNS = [
    {"equipment": "Centrifugal Pump", "keywords": ["pump", "centrifugal"], "recommendation": "Inspect impeller wear and bearing condition; verify seal integrity", "priority": "high", "hours": 4.0},
    {"equipment": "Air Compressor", "keywords": ["compressor", "air compressor"], "recommendation": "Replace air filters, check oil level, inspect safety valves", "priority": "medium", "hours": 2.0},
    {"equipment": "Industrial Boiler", "keywords": ["boiler", "steam"], "recommendation": "Conduct water treatment analysis and inspect burner assembly", "priority": "high", "hours": 8.0},
    {"equipment": "Electric Motor", "keywords": ["motor", "electric motor"], "recommendation": "Perform vibration analysis and thermal imaging inspection", "priority": "medium", "hours": 3.0},
    {"equipment": "Control Valve", "keywords": ["valve", "control valve"], "recommendation": "Calibrate actuator, check stem packing, verify positioner settings", "priority": "medium", "hours": 2.5},
    {"equipment": "Conveyor System", "keywords": ["conveyor", "belt"], "recommendation": "Inspect belt tension, rollers, and emergency stop mechanisms", "priority": "low", "hours": 1.5},
]


def generate_maintenance_recommendations(text: str, document_id: int, entities: dict) -> list[dict]:
    text_lower = text.lower()
    results = []
    found_equipment = set(entities.get("equipment", []))

    for pattern in MAINTENANCE_PATTERNS:
        keyword_hits = sum(1 for kw in pattern["keywords"] if kw in text_lower)
        equip_match = any(kw.lower() in str(found_equipment).lower() for kw in pattern["keywords"])

        if keyword_hits >= 1 or equip_match:
            confidence = min(0.95, 0.5 + keyword_hits * 0.15)
            results.append({
                "equipment": pattern["equipment"],
                "recommendation": pattern["recommendation"],
                "priority": pattern["priority"],
                "confidence": round(confidence, 2),
                "source_document_id": document_id,
                "estimated_downtime_hours": pattern["hours"],
                "next_due_date": datetime.utcnow() + timedelta(days=30 if pattern["priority"] == "high" else 60),
                "status": "open",
            })

    if not results and "maintenance" in text_lower:
        results.append({
            "equipment": "General Plant Equipment",
            "recommendation": "Review preventive maintenance schedule and update CMMS records",
            "priority": "medium",
            "confidence": 0.6,
            "source_document_id": document_id,
            "estimated_downtime_hours": 2.0,
            "next_due_date": datetime.utcnow() + timedelta(days=45),
            "status": "open",
        })

    return results[:5]
