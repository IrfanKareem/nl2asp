import json
import random


from utils.support_functions import load_dataset

FILENAME = "NL2CNL_FinalDataset.json"
OUTNAME = "NL2CNL_FinalDataset_with_predicates.json"
THRESHOLD = 0.65  # ---> perc of adding a pred or not


random.seed(1902)

ds = load_dataset(FILENAME)

def get_predicates(cnl):
        return [x for x in cnl.split(".") if "identified " in x]

def predicates_to_add(cnl):
    preds = get_predicates(cnl)
    preds_toadd = [x for x in preds if random.random() < THRESHOLD] 

    return f" {'. '.join(preds_toadd).strip().replace("  ", " ")}.\n" if len(preds_toadd) > 0 else ""


out = []

total_augmented = 0
for d in ds:
    if random.random() > 0.5:
        d["Id"] = d["Id"] + "A" # adding A in the id for Augmented
        d["added_predicates"] = True
        d["NL_V2"] = f"{predicates_to_add(d["CNL_V2"])}{d["NL_V2"]}"
        total_augmented += 1
    out.append(d)

def sort_key(item):
    added_preds = False
    id = item["Id"]
    if id.endswith("A"):
        id = id[:-1]
        added_preds = True
    parts = id.split('_')
    prefix = parts[0]
    code = int(parts[1]) 
    return (code, prefix, id, added_preds)

out = sorted(out, key=sort_key)

print(f"\x1b[34mIncreased to: {len(out)} elements.") #style points :)
print(f"\x1b[32mTotal_Size: {len(out)} Augmented_size: {total_augmented} Standard_size: {len(out) - total_augmented}.")

with open(OUTNAME, "w") as f:
    json.dump({"data_dict": out}, f, indent=4)