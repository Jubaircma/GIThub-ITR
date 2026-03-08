import json
from typing import Any, Optional


def find_first_value_by_key(element: Any, key: str) -> Optional[Any]:
    """Recursively search for the first occurrence of a key in a JSON structure."""
    if isinstance(element, dict):
        if key in element:
            return element[key]
        for value in element.values():
            result = find_first_value_by_key(value, key)
            if result is not None:
                return result
    elif isinstance(element, list):
        for item in element:
            result = find_first_value_by_key(item, key)
            if result is not None:
                return result
    return None


def find_values_by_key(element: Any, key: str) -> list:
    """Recursively search for all occurrences of a key in a JSON structure."""
    results = []
    
    if isinstance(element, dict):
        if key in element:
            results.append(element[key])
        for value in element.values():
            results.extend(find_values_by_key(value, key))
    elif isinstance(element, list):
        for item in element:
            results.extend(find_values_by_key(item, key))
    
    return results
