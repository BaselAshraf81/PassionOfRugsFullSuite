#!/usr/bin/env python3
"""
Excel File Merger for TrestleIQ Lead Processor
Merges all Excel files from a directory into a standardized format
"""

import pandas as pd
import glob
import os
from pathlib import Path

def standardize_columns(df, filename):
    """
    Standardize column names and create required columns for TrestleIQ processor
    Expected output columns: name, phone, address, city, state, zip, activity_score
    """
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Normalize column names to lowercase and handle spaces
    df.columns = df.columns.str.lower().str.strip()
    
    # Handle different column name variations
    column_mapping = {
        # Name variations
        'name': 'name',
        
        # Phone variations  
        'phone': 'phone',
        
        # Address variations
        'address': 'address',
        'address_1': 'address',
        
        # City variations
        'city': 'city',
        
        # State variations
        'state': 'state',
        
        # ZIP variations
        'zip': 'zip',
        
        # Activity score variations
        'activity_score': 'activity_score',
        'activity score': 'activity_score'
    }
    
    # Rename columns based on mapping
    df = df.rename(columns=column_mapping)
    
    # Ensure required columns exist
    required_columns = ['name', 'phone', 'address', 'city', 'state', 'zip', 'activity_score']
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = ''  # Add missing columns as empty
    
    # Handle special cases based on filename patterns
    if 'CA_LOW' in filename:
        # CA_LOW has uppercase columns
        if 'NAME' in df.columns:
            df['name'] = df['NAME']
        if 'PHONE' in df.columns:
            df['phone'] = df['PHONE']
        if 'ADDRESS' in df.columns:
            df['address'] = df['ADDRESS']
        if 'CITY' in df.columns:
            df['city'] = df['CITY']
        if 'STATE' in df.columns:
            df['state'] = df['STATE']
        if 'ZIP' in df.columns:
            df['zip'] = df['ZIP']
        if 'ACTIVITY SCORE' in df.columns:
            df['activity_score'] = df['ACTIVITY SCORE']
    
    # Handle address_2 field - combine with address if exists
    if 'address_2' in df.columns:
        # Combine address and address_2
        df['address'] = df['address'].astype(str) + ' ' + df['address_2'].fillna('').astype(str)
        df['address'] = df['address'].str.strip()
    
    # Handle missing ZIP in OH_LOW (it doesn't have zip column)
    if 'OH_LOW' in filename and 'zip' not in df.columns:
        df['zip'] = ''
    
    # Clean up data
    df['name'] = df['name'].fillna('').astype(str).str.strip()
    df['phone'] = df['phone'].fillna('').astype(str).str.strip()
    df['address'] = df['address'].fillna('').astype(str).str.strip()
    df['city'] = df['city'].fillna('').astype(str).str.strip()
    df['state'] = df['state'].fillna('').astype(str).str.strip()
    df['zip'] = df['zip'].fillna('').astype(str).str.strip()
    df['activity_score'] = pd.to_numeric(df['activity_score'], errors='coerce').fillna(0)
    
    # Return only the required columns
    return df[required_columns]

def merge_excel_files(source_dir, output_file):
    """
    Merge all Excel files from source directory into a single standardized file
    """
    source_path = Path(source_dir)
    excel_files = list(source_path.glob("*.xlsx"))
    
    if not excel_files:
        print(f"No Excel files found in {source_dir}")
        return
    
    print(f"Found {len(excel_files)} Excel files to merge")
    
    all_dataframes = []
    total_rows = 0
    
    for file_path in sorted(excel_files):
        filename = file_path.name
        print(f"\nProcessing: {filename}")
        
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            original_rows = len(df)
            print(f"  Original rows: {original_rows}")
            
            # Standardize columns
            df_standardized = standardize_columns(df, filename)
            standardized_rows = len(df_standardized)
            print(f"  Standardized rows: {standardized_rows}")
            
            # Add source file column for tracking
            df_standardized['source_file'] = filename
            
            all_dataframes.append(df_standardized)
            total_rows += standardized_rows
            
        except Exception as e:
            print(f"  ERROR processing {filename}: {e}")
            continue
    
    if not all_dataframes:
        print("No files were successfully processed")
        return
    
    # Combine all dataframes
    print(f"\nCombining {len(all_dataframes)} files...")
    merged_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Remove rows with missing critical data
    print(f"Total rows before cleaning: {len(merged_df)}")
    
    # Remove rows where both name and phone are empty
    merged_df = merged_df[~((merged_df['name'] == '') & (merged_df['phone'] == ''))]
    print(f"Rows after removing empty name+phone: {len(merged_df)}")
    
    # Remove rows where phone is empty (phone is required for TrestleIQ)
    merged_df = merged_df[merged_df['phone'] != '']
    print(f"Rows after removing empty phone: {len(merged_df)}")
    
    # Remove duplicates based on phone number
    before_dedup = len(merged_df)
    merged_df = merged_df.drop_duplicates(subset=['phone'], keep='first')
    after_dedup = len(merged_df)
    print(f"Rows after deduplication by phone: {after_dedup} (removed {before_dedup - after_dedup} duplicates)")
    
    # Sort by activity_score (lowest first, as program skips > 30)
    merged_df = merged_df.sort_values('activity_score')
    
    # Save to Excel
    print(f"\nSaving merged file to: {output_file}")
    
    # Reorder columns for TrestleIQ (remove source_file for final output)
    final_columns = ['name', 'phone', 'address', 'city', 'state', 'zip', 'activity_score']
    merged_df_final = merged_df[final_columns]
    
    merged_df_final.to_excel(output_file, index=False)
    
    print(f"✓ Merge complete!")
    print(f"✓ Final rows: {len(merged_df_final)}")
    print(f"✓ Output file: {output_file}")
    
    # Show activity score distribution
    print(f"\nActivity Score Distribution:")
    print(f"  0-10: {len(merged_df_final[merged_df_final['activity_score'] <= 10])}")
    print(f"  11-20: {len(merged_df_final[(merged_df_final['activity_score'] > 10) & (merged_df_final['activity_score'] <= 20)])}")
    print(f"  21-30: {len(merged_df_final[(merged_df_final['activity_score'] > 20) & (merged_df_final['activity_score'] <= 30)])}")
    print(f"  31+: {len(merged_df_final[merged_df_final['activity_score'] > 30])} (will be skipped by TrestleIQ)")
    
    return merged_df_final

def main():
    # Configuration
    source_directory = r"D:\Docs\PassionOfRugsDataProcessor\ZÿP OLACAK 3\30 and under\Score40"
    output_filename = "merged_leads_for_trestleiq.xlsx"
    
    print("TrestleIQ Excel File Merger")
    print("=" * 50)
    print(f"Source directory: {source_directory}")
    print(f"Output file: {output_filename}")
    print()
    
    # Check if source directory exists
    if not os.path.exists(source_directory):
        print(f"ERROR: Source directory does not exist: {source_directory}")
        return
    
    # Merge files
    try:
        merged_df = merge_excel_files(source_directory, output_filename)
        
        if merged_df is not None:
            print(f"\n✓ Success! Ready for TrestleIQ processing.")
            print(f"✓ Use file: {output_filename}")
            print(f"✓ Expected format: name, phone, address, city, state, zip, activity_score")
            
    except Exception as e:
        print(f"\n✗ Error during merge: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()