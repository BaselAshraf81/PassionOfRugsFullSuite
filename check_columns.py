import pandas as pd
import glob
import os

# Target directory with the data
target_dir = r"D:\Docs\PassionOfRugsDataProcessor\ZÿP OLACAK 3\30 and under\Score40"

# Get all Excel files in the target directory
excel_files = glob.glob(os.path.join(target_dir, "*.xlsx"))

print(f"Found {len(excel_files)} Excel files\n")

# Dictionary to store unique column sets
column_sets = {}

for file in sorted(excel_files):
    try:
        # Read just the first row to get column names
        df = pd.read_excel(file, nrows=0)
        columns = list(df.columns)
        
        print(f"\n{file}:")
        print(f"  Columns ({len(columns)}): {columns}")
        
        # Group files by their column structure
        col_tuple = tuple(columns)
        if col_tuple not in column_sets:
            column_sets[col_tuple] = []
        column_sets[col_tuple].append(file)
        
    except Exception as e:
        print(f"\n{file}: ERROR - {e}")

# Summary of unique column structures
print("\n" + "="*80)
print("SUMMARY - Unique Column Structures:")
print("="*80)

for i, (cols, files) in enumerate(column_sets.items(), 1):
    print(f"\nStructure #{i} ({len(files)} files):")
    print(f"  Columns: {list(cols)}")
    print(f"  Files: {', '.join(files)}")
