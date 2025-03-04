def spoof_tool_steps(tool_json):
    tool = tool_json.copy()
    tool["transformations"] = {
        "steps": [
            {
                "transformation": "js_code_transformation",
                "display_name": "Spoofed Tool",
                "name": "spoofed_tool",
                "params": {
                    "code": "return params.spoof_input;"
                }
            }
        ],
        "output": {
            "output": "{{spoofed_tool.transformed}}"
        }
    }
    tool["output_schema"] = {}

    return tool


def remove_fixed_tool_input(tool_json):
    """ Removes fixed parameters from a tool's configuration. """
    tool = tool_json.copy()
    
    params_schema = tool.get("params_schema", {})
    properties = params_schema.get("properties", {})
    fixed_params = []

    for param_name, param_config in list(properties.items()):
        metadata = param_config.get("metadata", {})
        is_fixed = metadata.get("is_fixed_param", False)
        
        if is_fixed:
            fixed_params.append(param_name)
            properties.pop(param_name)

    if "required" in params_schema:
        params_schema["required"] = [param for param in params_schema["required"] if param not in fixed_params]

    return tool


def create_fixed_spoofed_input(tool_json, type):
    """ Adds a fixed parameter input to spoof the output of a tool. """
    tool = tool_json.copy()
    if "params_schema" not in tool:
        tool["params_schema"] = {}
    
    if "properties" not in tool["params_schema"]:
        tool["params_schema"]["properties"] = {}

    tool["params_schema"]["properties"]["spoof_input"] = {
        "type": type,
        "title": "Spoofed Input",
        "description": "Fixed parameter used to spoof the tool output as per the historical runs.",
        "metadata": {
            "is_fixed_param": True,
            "is_history_excluded": True
        }
    }
    
    if "required" not in tool["params_schema"]:
        tool["params_schema"]["required"] = []
    tool["params_schema"]["required"].append("spoof_input")
    
    return tool


def spoof_tools(tool_jsons:list, output_type:str='object'):
    spoofed_tool = []
    for tool_json in tool_jsons:
        tool = spoof_tool_steps(tool_json)
        tool = remove_fixed_tool_input(tool)
        tool = create_fixed_spoofed_input(tool, output_type)
        tool['state_mapping'] = {
            "spoof_input": "params.spoof_input",
            "spoofed_tool": "steps.spoofed_tool.output"
        }
        spoofed_tool.append(tool)
    return spoofed_tool
