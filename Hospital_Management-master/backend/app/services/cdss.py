import re
from typing import Dict, Any, List, Optional

# Demonstration Knowledge Base
CROSS_ALLERGY_MAP = {
    "penicillin": ["amoxicillin", "ampicillin", "augmentin", "piperacillin", "clavulanate", "penicillin"],
    "amoxicillin": ["penicillin", "ampicillin", "augmentin"],
    "sulfa": ["bactrim", "septra", "sulfamethoxazole", "trimethoprim", "sulfasalazine"],
    "aspirin": ["ibuprofen", "naproxen", "diclofenac", "ketorolac", "nsaid", "aspirin"],
    "nsaid": ["aspirin", "ibuprofen", "naproxen", "diclofenac"],
    "latex": ["latex"],
}

DRUG_DRUG_CONFLICTS = [
    {
        "drugs": ["warfarin", "aspirin"],
        "severity": "CRITICAL",
        "description": "High risk of life-threatening gastrointestinal hemorrhage and bleeding events."
    },
    {
        "drugs": ["metformin", "contrast"],
        "severity": "CRITICAL",
        "description": "Risk of contrast-induced acute renal failure leading to fatal lactic acidosis."
    },
    {
        "drugs": ["sildenafil", "nitroglycerin"],
        "severity": "FATAL",
        "description": "Profound synergistic vasodilation causing irreversible hypotension and cardiovascular collapse."
    },
    {
        "drugs": ["ace inhibitor", "spironolactone"],
        "severity": "WARNING",
        "description": "Risk of severe hyperkalemia and cardiac dysrhythmias."
    }
]

def check_allergy_and_drug_safety(patient_allergies_str: Optional[str], prescription_text: str) -> Dict[str, Any]:
    """
    Evaluates prescription against known patient allergies and drug-drug conflicts.
    IMPORTANT: This is a demonstration clinical decision support feature.
    All prescriptions require qualified clinician review.
    """
    alerts: List[Dict[str, str]] = []
    
    rx_lower = prescription_text.lower()
    
    # 1. Check patient allergies
    if patient_allergies_str:
        allergies = [a.strip().lower() for a in patient_allergies_str.split(",") if a.strip()]
        for allergen in allergies:
            for group_key, reactive_drugs in CROSS_ALLERGY_MAP.items():
                if group_key in allergen:
                    for drug in reactive_drugs:
                        if re.search(r'\b' + re.escape(drug) + r'\b', rx_lower):
                            alerts.append({
                                "type": "ALLERGY_CONFLICT",
                                "severity": "HIGH",
                                "title": f"Documented Allergy Alert: {allergen.title()}",
                                "message": f"Prescription contains '{drug.title()}' which presents high cross-reactivity risk with documented patient allergen '{allergen.title()}'."
                            })
                            break
    
    # 2. Check drug-drug conflicts
    for conflict in DRUG_DRUG_CONFLICTS:
        matches = [d for d in conflict["drugs"] if re.search(r'\b' + re.escape(d) + r'\b', rx_lower)]
        if len(matches) == len(conflict["drugs"]):
            alerts.append({
                "type": "DRUG_INTERACTION",
                "severity": conflict["severity"],
                "title": f"Dangerous Drug Interaction: {' + '.join(m.title() for m in matches)}",
                "message": conflict["description"]
            })
            
    return {
        "safe": len(alerts) == 0,
        "disclaimer": "DEMONSTRATION CDSS: Unvalidated automated rules. Qualified clinician review required.",
        "alerts": alerts
    }

def evaluate_vitals_string(vitals_str: Optional[str]) -> Dict[str, Any]:
    """Parse vitals summary string and evaluate clinical flags."""
    if not vitals_str:
        return {"status": "Not recorded", "flags": []}
    
    flags = []
    
    # BP extraction
    bp_match = re.search(r'(\d{2,3})\s*/\s*(\d{2,3})', vitals_str)
    if bp_match:
        sys = int(bp_match.group(1))
        dia = int(bp_match.group(2))
        if sys >= 180 or dia >= 120:
            flags.append({"param": "BP", "tag": "Hypertensive Crisis", "severity": "danger"})
        elif sys >= 140 or dia >= 90:
            flags.append({"param": "BP", "tag": "Stage 2 Hypertension", "severity": "warning"})
        elif sys >= 130 or dia >= 80:
            flags.append({"param": "BP", "tag": "Stage 1 Hypertension", "severity": "info"})
    
    # HR extraction
    hr_match = re.search(r'HR[:\s]+(\d{2,3})', vitals_str, re.IGNORECASE)
    if hr_match:
        hr = int(hr_match.group(1))
        if hr > 100:
            flags.append({"param": "HR", "tag": "Tachycardia", "severity": "warning"})
        elif hr < 60:
            flags.append({"param": "HR", "tag": "Bradycardia", "severity": "info"})
    
    # SpO2 extraction
    spo2_match = re.search(r'SpO2[:\s]+(\d{2,3})', vitals_str, re.IGNORECASE)
    if spo2_match:
        spo2 = int(spo2_match.group(1))
        if spo2 < 92:
            flags.append({"param": "SpO2", "tag": "Severe Hypoxia", "severity": "danger"})
        elif spo2 < 95:
            flags.append({"param": "SpO2", "tag": "Borderline SpO2", "severity": "warning"})

    return {
        "status": "Recorded",
        "flags": flags,
        "raw": vitals_str
    }
