import pandas as pd

# --- LOAD DATA ---
try:
    df = pd.read_csv('drugs.csv')
except FileNotFoundError:
    print("❌ Error: 'drugs.csv' not found. Make sure it's in the same folder as this script.")
    exit()

# --- CLEANING & FORMATTING ---
df['TreatsDisease'] = df['TreatsDisease'].str.strip().str.lower()
df['DrugName'] = df['DrugName'].str.strip()
df['ProteinTarget'] = df['ProteinTarget'].str.strip()

# --- SET SOURCE DISEASE ---
source_disease = "hypertension"
print(f"\n🔍 Starting with drugs for: {source_disease.title()}")

# --- STEP 1: Get drugs for source disease ---
hypertension_drugs = df[df['TreatsDisease'] == source_disease]
protein_targets = hypertension_drugs['ProteinTarget'].unique()

print(f"\n🧬 Found protein targets for {source_disease.title()}: {list(protein_targets)}")

# --- STEP 2: Find entries sharing those targets ---
potential_leads = df[df['ProteinTarget'].isin(protein_targets)]

# --- STEP 3: Remove original disease entries ---
repurposing_candidates = potential_leads[potential_leads['TreatsDisease'] != source_disease]
repurposing_candidates = repurposing_candidates.drop_duplicates()

# --- STEP 4: Display Results ---
print("\n📋 --- Potential Drug Repurposing Candidates ---")
repurposed_list = []

if repurposing_candidates.empty:
    print("⚠️ No repurposing candidates found in this dataset.")
else:
    for target in protein_targets:
        print(f"\n🔗 Based on shared target: {target}")
        
        # Get the original drug linked to this target for the source disease
        original_drug_series = df[(df['TreatsDisease'] == source_disease) & (df['ProteinTarget'] == target)]['DrugName']
        if not original_drug_series.empty:
            original_drug = original_drug_series.iloc[0]
        else:
            continue  

        # Find new diseases for this target
        new_diseases = repurposing_candidates[repurposing_candidates['ProteinTarget'] == target]

        if not new_diseases.empty:
            for _, row in new_diseases.iterrows():
                print(f"💊 '{original_drug}' (for {source_disease.title()}) may also treat '{row['TreatsDisease'].title()}'")
                repurposed_list.append({
                    'Original Drug': original_drug,
                    'Protein Target': target,
                    'Potential New Disease': row['TreatsDisease'].title()
                })
        else:
            print("⚠️ No additional disease found for this target.")

# --- STEP 5: Export to CSV ---
if repurposed_list:
    repurposed_df = pd.DataFrame(repurposed_list)
    repurposed_df.to_csv("repurposing_results.csv", index=False)
    print("\n✅ Results exported to 'repurposing_results.csv'")
