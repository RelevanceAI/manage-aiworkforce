import os
import re
import json


def make_valid_ref_name(name):
    name = name.replace(" ", "-")
    name = re.sub(r"[^\w-]", "", name)
    return name

def open_object_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def save_object_file(filepath, json):
    with open(filepath, "w") as f:
        json.dump(json, f, indent=4)

def open_all_object_files(folderpath):
    object_jsons = []
    for file in os.listdir(folderpath):
        if file.endswith(".json"):
            with open(f"{folderpath}/{file}", "r") as f:
                object_jsons.append(json.load(f))
    return object_jsons

def clean_filename(f, object_type):
    if object_type == "tools":
        title = f["title"]
        uid = f["studio_id"]
    elif object_type == "agents":
        title = f["name"]
        uid = f["agent_id"]
    title = re.sub(r"[^\w\-_.]", "", title.replace(" ", "-")).lower()
    object_id = uid.replace("/", "_").replace(".", "_").replace(":", "_")

    return f'{title}--{object_id}.json'

def remove_objects_changing_fields(object_jsons):
    for obj in object_jsons:
        if "metrics" in obj: del obj["metrics"]
        if "update_date_" in obj: del obj["update_date_"]
        if "insert_date_" in obj: del obj["insert_date_"]
        if "machine_user_id" in obj: del obj["machine_user_id"]
        if "update_date" in obj: del obj["update_date"]
        if "dateAdded" in obj: del obj["dateAdded"]
        if "metadata" in obj and obj.get('metadata', {}).get('last_run_date'): del obj['metadata']['last_run_date']
        if "metadata" in obj and obj.get('metadata', {}).get('clone_count'): del obj['metadata']['clone_count']
    return object_jsons

def update_objects_metadata(object_jsons, prod_project_id):
    for obj in object_jsons:
        obj['public'] = False
        obj['project'] = prod_project_id
        object_id = obj.get('studio_id', obj.get('agent_id', obj.get('knowledge_id')))
        obj['_id'] = f"{prod_project_id}_-_{object_id}"
        if 'actions' in obj and isinstance(obj['actions'], list):
            for action in obj['actions']:
                action['project'] = prod_project_id
    return object_jsons

def save_all_objects(object_jsons, folderpath, object_type):
    os.makedirs(folderpath, exist_ok=True)
    for obj in object_jsons:
        file = clean_filename(obj, object_type)
        with open(f"{folderpath}/{file}", "w") as f:
            json.dump(obj, f, indent=4)

def remove_local_files_not_in_objects(objects, object_type, filepath):
    """ Designed to remove files that have had their object deleted from Relevance AI - to ensure deletion syncs """
    current_list = []
    for obj in objects:
        current_list.append(clean_filename(obj, object_type))
    
    if not os.path.exists(filepath):
        return

    for file in os.listdir(filepath):
        if file not in current_list and file.endswith(".json"):
            os.remove(f"{filepath}/{file}")
