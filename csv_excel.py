import pandas as pd

# Function to load CSV files
def load_csv(file_path):
    return pd.read_csv(file_path)

def save_to_excel(df, file_path):
    df.to_excel(file_path, index=False)

csv1 = load_csv('output.csv')
save_to_excel(csv1, 'price_compare.xlsx')

print("CSV saved as Excel successfully!")
