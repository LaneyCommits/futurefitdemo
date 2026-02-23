#!/usr/bin/env python3
"""Export schools data to JSON for static site. Run from project root: python3 scripts/export_schools_json.py"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schools.schools_data import SCHOOLS

data = [
    {
        "id": s["id"],
        "name": s["name"],
        "city": s["city"],
        "state": s["state"],
        "type": s["type"],
        "size": s["size"],
        "tuition": s["tuition"],
        "tuition_in": s["tuition_in"],
        "acceptance_rate": s["acceptance_rate"],
        "strong_majors": s["strong_majors"],
        "highlight": s["highlight"],
        "url": s["url"],
        "image": s["image"],
    }
    for s in SCHOOLS
]
print(json.dumps(data, indent=2))
