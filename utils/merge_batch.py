import json
import pandas as pd
from support_functions import load_dataset, check_asp_syntax

def parse_batch(filepath):
    results = {}
    with open(filepath) as f:
        for line in f:
            entry = json.loads(line)
            cid = entry["custom_id"]
            try:
                text = entry["response"]["body"]["output"][0]["content"][0]["text"]
            except (KeyError, IndexError, TypeError):
                text = None
            results[cid] = text
    return results

if __name__ == "__main__":

    ds = load_dataset("utils/test_set.json")

    batch1 = parse_batch("utils/out_gpt5.2.jsonl")
    batch2 = parse_batch("utils/out_gpt5.2_withPreds.jsonl")

    out = []
    merged_results = {}
    for entry in ds:
        entry["gpt5.2"] = batch1[entry["ID"]]
        entry["gpt5.2_syntax"] = check_asp_syntax(entry["gpt5.2"])
        entry["gpt5.2_eval"] = None
        entry["gpt5.2_wpreds"] = batch2[entry["ID"]]
        entry["gpt5.2_wpreds_syntax"] = check_asp_syntax(entry["gpt5.2_wpreds"])
        entry["gpt5.2_wpreds_eval"] = None
        out.append(entry)

    out = pd.DataFrame(out)
    out.to_excel("utils/GPT5_results.xlsx", index=False)
