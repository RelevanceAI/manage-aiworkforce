import requests
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any
import uuid

def get_all_knowledge(region_id, project_id, api_key):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/sets/list"
    body = {
        "filters": [],
        "sort": [{"update_date":"desc"}]
    }
    response = requests.post(path, json=body, headers=headers)

    return response.json().get("results", [])


def get_knowledge(region_id:str, project_id:str, api_key:str, knowledge_set: str, max_results: int = 5000):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/list"
    body = {
        "knowledge_set": knowledge_set,
        "page_size": max_results,
        "sort": [{"insert_date_": "desc"}]
    }
    response = requests.post(path, data=json.dumps(body), headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    return {"error": response.text}


def delete_knowledge(region_id:str, project_id:str, api_key:str, knowledge_set: str) -> bool:
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/sets/delete"
    body = {"knowledge_set": knowledge_set}
    response = requests.post(path, json=body, headers=headers)

    return response.status_code == 200


@dataclass
class KnowledgeDocument:
    """Represents a document to be added to a knowledge store."""
    value: Dict[str, Any] # records with column names as keys and record data as values
    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "document"


def add_knowledge_data(region_id: str, project_id: str, api_key: str, knowledge_id: str, records: List[Dict[str, Any]]) -> dict:
    headers = {"Authorization": f"{project_id}:{api_key}", "Content-Type": "application/json"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/add"
    
    documents = [KnowledgeDocument(value=item) for item in records]
    
    body = {
        "data": [doc.__dict__ for doc in documents],
        "knowledge_set": knowledge_id
    }
    
    response = requests.post(path, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return {"error": response.text, "status_code": response.status_code}



def get_knowledge_metadata(region_id:str, project_id:str, api_key:str, knowledge_set: str):
    headers = {"Authorization": f"{project_id}:{api_key}"}
    base_url = f"https://api-{region_id}.stack.tryrelevance.com/latest"
    path = f"{base_url}/knowledge/sets/{knowledge_set}/get_metadata"
    response = requests.get(path, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}
