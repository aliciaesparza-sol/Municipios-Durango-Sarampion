import pandas as pd

dst_path = 'dst_temp.xlsx'
df = pd.read_excel(dst_path, sheet_name='Desglose')

# Check if TIERRAS COLORADAS exists
exists = df[df['Localidad'].str.upper().str.strip() == 'TIERRAS COLORADAS']
if not exists.empty:
    print("Tierras Coloradas already exists in destination:")
    print(exists)
else:
    print("Tierras Coloradas not found in destination.")
