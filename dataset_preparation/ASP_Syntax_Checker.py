import pandas as pd
from utils.support_functions import check_asp_syntax

####################################
############# SETTINGS #############
####################################

BASE_PATH = "Results/stageX/"
OUTPUT_FILE = BASE_PATH + "DESIRED_FILENAME.xlsx"
MODELS_NAMES = {"MODEL_NAME": "RESULTS_FILENAME.csv",
                }

####################################

outdf = pd.DataFrame(columns=["ID, Category, NL, ASP"])


for MODEL_NAME in MODELS_NAMES.keys():
    df = pd.read_csv(BASE_PATH + MODELS_NAMES[MODEL_NAME])
    df.rename({"Natural Language": "NL", "Actual ASP": "ASP"}, axis=1, inplace=True)

    if outdf.empty:
        outdf = df[["ID", "Category", "NL", "ASP"]].copy()
    outdf[f"{MODEL_NAME}"] = df["Predicted ASP"]
    outdf[f"{MODEL_NAME}_syntax"] = outdf[F"{MODEL_NAME}"].apply(check_asp_syntax)

    # summary stats
    print("~" * 22)
    print(f"\nModel: {MODEL_NAME}")
    print(f"\nTotal          : {len(outdf)}")
    print(f"Syntax Valid   : {outdf[f"{MODEL_NAME}_syntax"].sum()}")
    print(f"Syntax Invalid : {len(outdf) - outdf[f"{MODEL_NAME}_syntax"].sum()}")
    print("~" * 22)
outdf.to_excel(OUTPUT_FILE, index=False)
print(f"Saved in {OUTPUT_FILE}")