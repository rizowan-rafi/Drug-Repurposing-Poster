import pandas as pd

# Load our sample database from the CSV file
try:
    df = pd.read_csv('drugs.csv')
except FileNotFoundError:
    print("Error: 'drugs.csv' not found. Make sure it's in the same folder as this script.")
    exit()

# --- THE LOGIC STARTS HERE ---

# 1. Define our starting point: the disease we already have drugs for.
source_disease = "Hypertension"
print(f"Starting with drugs for: {source_disease}\n")

# 2. Find all protein targets that are affected by drugs for this disease.
# We filter the database to get only the rows for Hypertension drugs.
hypertension_drugs = df[df['TreatsDisease'] == source_disease]
# From those rows, we get a list of the unique protein targets.
protein_targets = hypertension_drugs['ProteinTarget'].unique()

print(f"Found protein targets for {source_disease}: {list(protein_targets)}\n")

# 3. Now, find all other diseases linked to these same protein targets.
# We search the whole database for any entry where the protein is one of our targets.
potential_leads = df[df['ProteinTarget'].isin(protein_targets)]

# 4. Clean up and display the results.
# We don't want to suggest the original disease, so we remove it.
repurposing_candidates = potential_leads[potential_leads['TreatsDisease'] != source_disease]


print("--- Potential Drug Repurposing Candidates ---")
if repurposing_candidates.empty:
    print("No potential repurposing candidates found in this dataset.")
else:
    # We group the results to make them easy to read.
    for target in protein_targets:
        print(f"\n--- Based on shared target: {target} ---")
        
        # Find the original drug for this target
        # Using .iloc[0] to get the first drug if multiple exist for the same target
        original_drug_series = df[(df['TreatsDisease'] == source_disease) & (df['ProteinTarget'] == target)]['DrugName']
        if not original_drug_series.empty:
            original_drug = original_drug_series.iloc[0]
        else:
            continue # Should not happen based on logic, but good practice

        # Find the new diseases for this target
        new_diseases_info = repurposing_candidates[repurposing_candidates['ProteinTarget'] == target]
        
        if not new_diseases_info.empty:
            for index, row in new_diseases_info.iterrows():
                print(f"The drug '{original_drug}' (for {source_disease}) could potentially be used for '{row['TreatsDisease']}'")
        else:
            print("No other diseases found for this target in the dataset.")
