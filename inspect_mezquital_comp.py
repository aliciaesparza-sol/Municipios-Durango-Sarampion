import pandas as pd
import json

path = r'Mezquital_Comp_Temp.xlsx'

try:
    xl = pd.ExcelFile(path)
    info = {
        "sheets": xl.sheet_names,
        "previews": {}
    }
    for sheet in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet, nrows=10)
        info["previews"][sheet] = df.astype(str).values.tolist()
        info["columns"] = {sheet: df.columns.tolist()}
        
    with open('mezquital_comp_info.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
