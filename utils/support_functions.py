import os
import json
import clingo
import requests

def load_dataset(filename : str):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            dataset = full_data.get("data_dict", [])
            print(f"Dataset with: {len(dataset)} items ")
            return dataset
    except FileNotFoundError:
        print(f"Error: file not found")
        return []
    except json.JSONDecodeError:
        print(f"Errore: {filename} not a json")
        return []
    
def check_cnl(cnl : str, endpoint : str):
    try:
        payload = json.dumps({"cnls": cnl})
        headers = {
            'X-API-KEY': '', 
            # local API key to connect to the CNL2ASP endpoint.
            # This is part of another project, so please refer to Caruso et al. to serve the tool.
            # Paper:                https://doi.org/10.1017/S1471068423000388
            # github for the repo:  https://github.com/dodaro/cnl2asp 
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", endpoint, headers=headers, data=payload)

        return response.json()['asp'].replace('\n', '')


    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except json.JSONDecodeError:
        print("Error: The server returned a non-JSON response.")
        print(f"Actual response: {response.text}")
    except Exception as e:
        print(response.json().keys())
        print("Error checking CNL:", e)
    
    return 'ERROR!'

def load_cache(filename: str):
    if not os.path.exists(filename):
        print("Creating new cache file")
        return {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cache = {}
    for k, v in data.items():
        parts = k.split('|')
        cache[(parts[0], parts[1])] = v
    print(f"Loaded {len(cache)} elements in cache.")
    return cache

def save_cache(cache : dict, filename: str):
    serializable_cache = {f"{k[0]}|{k[1]}": v for k, v in cache.items()}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(serializable_cache, f, indent=4, ensure_ascii=False)
    print(f"Cache in {filename}")


def check_asp_syntax(program_str: str) -> bool:
    if not program_str.strip():
        return False

    try:
        ctl = clingo.Control(["--warn=none"])
        ctl.add("base", [], program_str)
        ctl.ground([("base", [])])
    except Exception:
        return False

    return True