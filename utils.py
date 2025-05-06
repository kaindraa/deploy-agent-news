import re
from typing import List
def clean_markdown(s: str) -> str:
    return re.sub(r"^```(?:markdown)?\n?|```$", "", s.strip(), flags=re.MULTILINE)

def clean_json_string(s: str) -> str:
    return re.sub(r"```(?:json)?|```", "", s).strip()