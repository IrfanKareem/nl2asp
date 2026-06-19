import json

from support_functions import load_dataset

FILENAME = "test_set_with_predicates.json"


MODEL = "gpt-5.2"
FILEPOSTFIX_MODEL = "gpt-5.2"


SYSTEM_PROMPT_REPHRASE = {
 "role": "system",
  "content": '''You are an expert in Translating the Natural language (NL) into Answer Set Programming (ASP). Always provide precise, syntactically correct translations of NL into ASP. Only reply with the Answer Set Programming rule, without adding ANY other text.
'''} # prompt for gpt5.2

dataset = load_dataset(FILENAME)

lines = []
for ins in dataset:

             
    user_content = {"role": "user",
                "content":f"Translate the following rule: {ins['NL_V2']}"}

    tp = {
		"custom_id": ins['ID'],
		"method": "POST",
		"url": "/v1/responses",
		"body": {
            "model": MODEL,
            "input": [
                SYSTEM_PROMPT_REPHRASE,
                user_content
            ],
            "max_output_tokens": 5000      
		}
    }
	
    lines.append(tp)

with open(FILENAME.replace(".json", f"_batch_{FILEPOSTFIX_MODEL}.jsonl"), "w", encoding="utf-8") as file:
    for line in lines:
        json.dump(line, file, ensure_ascii=False)
        file.write('\n')