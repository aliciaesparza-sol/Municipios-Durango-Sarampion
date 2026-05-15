import pandas as pd

src_path = 'src_temp.xlsx'
df = pd.read_excel(src_path, sheet_name='Concentrado')

# Find row for TIERRAS COLORADAS
row = df[df.iloc[:, 2] == 'TIERRAS COLORADAS'].iloc[0]

# Extract the "Población Vacunada" section
# Based on the headers inspection:
# Set 1 (Encontrada): 8 columns + TOTAL
# Set 2 (Antecedente): 8 columns + TOTAL
# Set 3 (Sin Antecedente): 8 columns + TOTAL
# Set 4 (Vacunada): 8 columns + TOTAL
# Wait, let's just find the columns by name if possible, or index.
# The headers in the inspection were:
# 1177: "6 a 11 meses" (Set 4 start)
# 1178: "1 año"
# 1179: "2 a 4 años"
# 1180: "5 a 9 años"
# 1181: "10 a 19 años"
# 1182: "20 a 39 años"
# 1183: "40 a 49 años"
# 1184: "TOTAL"

# Let's find the indices. 
# "Población Vacunada" usually follows "Población sin antecedente".
# Let's print all values for that row to be sure.
print("Full Row for Tierras Coloradas:")
for i, val in enumerate(row):
    print(f"{i}: {val}")
