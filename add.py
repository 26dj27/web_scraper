import pandas as pd

csv1 = "updated_file.csv" 
csv2 = "output.csv" 

data1 = pd.read_csv(csv1)
data2 = pd.read_csv(csv2, on_bad_lines='skip') 
data1["search_number"] = data1["search_number"].astype(str)
data2["search_number"] = data2["search_number"].astype(str)
merged_data = pd.merge(data1, data2, on="search_number", how="inner")
output_file = "merged_data.csv"
merged_data.to_csv(output_file, index=False, encoding="utf-8")

print(f"Merged data saved to {output_file}")
