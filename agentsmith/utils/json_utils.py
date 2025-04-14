from typing import Any, Sequence, Mapping


def json_get(data: Any, path: str, default: Any = None) -> Any:
    """Safely navigate a nested structure using a dot-separated path."""
    parts = path.split('.')
    current_data = data
    for part in parts:
        if isinstance(current_data, Mapping):
            if part in current_data:
                current_data = current_data[part]
            else:
                return default
        elif isinstance(current_data, Sequence) and not isinstance(current_data, str):
            try:
                idx = int(part)
                if 0 <= idx < len(current_data):
                    current_data = current_data[idx]
                else:
                    return default
            except (ValueError, IndexError):
                return default
        else:
            return default
    return current_data


def update_json(data: Any, path: str, value: Any) -> Any:
    """Safely update a value in a nested structure using a dot-separated path."""
    parts = path.split('.')
    current_level = data
    for i, part in enumerate(parts[:-1]):
        next_level_is_list = parts[i+1].isdigit()
        
        if isinstance(current_level, dict):
            if part not in current_level:
                current_level[part] = [] if next_level_is_list else {}
            current_level = current_level[part]
        elif isinstance(current_level, list):
            try:
                idx = int(part)
                while len(current_level) <= idx:
                      current_level.append(None) # Pad with None if index out of bounds
                if current_level[idx] is None: # Overwrite None if needed
                    current_level[idx] = [] if next_level_is_list else {}
                current_level = current_level[idx]
            except ValueError:
                # Handle cases where part is not an integer for a list - potentially create a dict?
                # For now, let's raise an error or handle as per desired logic.
                # Here we might replace the list element with a dict if needed.
                raise TypeError(f"Cannot access non-integer index '{part}' in list for path '{path}'")
        else:
             raise TypeError(f"Cannot traverse path '{path}' at part '{part}'. Current level is not a dict or list.")

    last_part = parts[-1]
    if isinstance(current_level, dict):
        current_level[last_part] = value
    elif isinstance(current_level, list):
        try:
            idx = int(last_part)
            while len(current_level) <= idx:
                current_level.append(None)
            current_level[idx] = value
        except ValueError:
             raise TypeError(f"Cannot use non-integer index '{last_part}' for list assignment at path '{path}'")
    else:
        # This should ideally not happen if the traversal worked
        raise TypeError(f"Cannot set value at path '{path}'. Final level is not a dict or list.")

    return data # Return the modified root data structure
