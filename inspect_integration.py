import pandas as pd
import json

src_path = 'src_temp.xlsx'
dst_path = 'dst_temp.xlsx'

info = {"src": {}, "dst": {}}

try:
    # Inspect Source
    src_xl = pd.ExcelFile(src_path)
    info["src"]["sheets"] = src_xl.sheet_names
    for sheet in src_xl.sheet_names:
        df = pd.read_excel(src_xl, sheet_name=sheet, nrows=20)
        info["src"][sheet] = {
            "columns": df.columns.tolist(),
            "preview": df.astype(str).values.tolist()
        }
        
    # Inspect Destination
    dst_xl = pd.ExcelFile(dst_path)
    info["dst"]["sheets"] = dst_xl.sheet_names
    for sheet in dst_xl.sheet_names:
        df = pd.read_excel(dst_xl, sheet_name=sheet, nrows=20)
        info["dst"][sheet] = {
            "columns": df.columns.tolist(),
            "preview": df.astype(str).values.tolist()
        }

    with open('integration_info.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
