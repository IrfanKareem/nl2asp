import requests
import pandas as pd
from tqdm import tqdm
from utils.support_functions import load_dataset

INPUT_FILENAMES = ["test_set.json", "test_set_with_predicates.json"]

MODELS = ["qwen3.5:9B", "nchapman/ministral-8b-instruct-2410", "llama3.1:8b", "qwen3.5:9B_think"]
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
TIMEOUT_MS = 300  # timeout in seconds

SYSTEM_PROMPT = "You are an expert in Translating the Natural language (NL) into Answer Set Programming (ASP) translation. Always provide precise, syntactically and semantically correct translations of NL into ASP. Only return the ASP rule, without any additional content. DO NOT ADD ANY EXPLANATION OR COMMENT. The ASP rule should be in the format of a single line, without any line breaks. Do not add unnecessary punctuation or formatting. **KEEP THE THINKING SHORT**. Focus solely on the translation task and ensure that the output is a valid ASP rule that accurately represents the meaning of the input NL sentence."

tqdm.pandas()


def ollama_inference(nl: str, model: str) -> str:

    prompt = f"Write the Answer Set Programming (ASP) rule for the following natural language sentence: {nl}\n"
        
    try:
        response = requests.post(
            OLLAMA_ENDPOINT,
            headers={"Content-Type": "application/json"},
            json={
                "model": model,
                "stream": False,
                "system": SYSTEM_PROMPT,
                "prompt": prompt,
                "think": ("think" in model),
            },
            timeout=TIMEOUT_MS
        )
        # response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.Timeout:
        return "TIMEOUT"


if __name__ == "__main__":

    for INPUT_FILENAME in INPUT_FILENAMES:
        ds = load_dataset(INPUT_FILENAME)
        ds = pd.DataFrame(ds)

        for m in MODELS:
            ds[m] = ds["NL_V2"].progress_apply(lambda x: ollama_inference(x, m))

        print(ds.head())
        
        ds.to_excel(f"inference_phase4({INPUT_FILENAME.replace(".json", "")}).xlsx", index=False)