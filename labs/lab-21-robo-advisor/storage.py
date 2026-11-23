"""
FIN 43900 — AI Finance Applications
Module: Robo Advisor State Persistence & Session Recovery
Author: Oladapo Olaniyan
Date: November 2026

Addresses Dr. Z's key enhancement recommendation: saving user questionnaire
progress and portfolio state across runs to prevent repetitive questionnaire data entry.
"""

import os
import json
from datetime import datetime
from typing import List, Optional
from models import PortfolioPreference, FullRoboAdvisorReport

STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_profiles")
os.makedirs(STORAGE_DIR, exist_ok=True)
DEFAULT_PROFILE_PATH = os.path.join(STORAGE_DIR, "last_session.json")


def save_profile(preference: PortfolioPreference, filename: Optional[str] = None) -> str:
    """Saves user questionnaire preferences to a JSON file."""
    if filename is None:
        filename = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    path = os.path.join(STORAGE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(preference.model_dump_json(indent=2))
        
    # Also save to last_session.json for immediate resumption
    with open(DEFAULT_PROFILE_PATH, "w", encoding="utf-8") as f:
        f.write(preference.model_dump_json(indent=2))
        
    return path


def load_profile(path: Optional[str] = None) -> Optional[PortfolioPreference]:
    """Loads saved user preferences from file."""
    target_path = path or DEFAULT_PROFILE_PATH
    if not os.path.exists(target_path):
        return None
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return PortfolioPreference.model_validate(data)
    except Exception:
        return None


def list_saved_profiles() -> List[str]:
    """Returns a list of available saved profile filenames."""
    if not os.path.exists(STORAGE_DIR):
        return []
    files = [f for f in os.listdir(STORAGE_DIR) if f.endswith(".json")]
    files.sort(reverse=True)
    return files


def save_report_json(report: FullRoboAdvisorReport, filename: Optional[str] = None) -> str:
    """Saves full robo-advisor report with all agent verdicts to JSON."""
    if filename is None:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(STORAGE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))
    return path
