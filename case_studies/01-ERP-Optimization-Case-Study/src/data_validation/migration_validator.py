"""
==============================================================================================
Script: migration_validator.py
Description: Data validation pipeline used during the Logo Tiger 3 ERP implementation.
             Ingests legacy system CSV exports, validates referential integrity, formats
             dates, and flags anomalies before insertion into the new Oracle DB.
Author: Hajimammad Aliyev
==============================================================================================
"""

import pandas as pd
import numpy as np
import logging
import sys

# Configure logging
logging.basicConfig(
    filename='migration_validation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_data(filepath: str) -> pd.DataFrame:
    """Loads legacy CSV data."""
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Successfully loaded {len(df)} records from {filepath}")
        return df
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")
        sys.exit(1)

def validate_and_clean(df: pd.DataFrame, master_customer_ids: set) -> pd.DataFrame:
    """
    Applies business rules to clean and validate the dataset.
    """
    initial_count = len(df)
    
    # 1. Standardize Date Formats (legacy system used mixed formats)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    
    # Drop rows where date couldn't be parsed
    invalid_dates = df['transaction_date'].isna().sum()
    df = df.dropna(subset=['transaction_date'])
    logging.warning(f"Dropped {invalid_dates} records due to invalid date formats.")
    
    # 2. Referential Integrity Check (Foreign Key Validation)
    # Ensure all sales records map to a valid customer ID in the master list
    orphaned_records = df[~df['customer_id'].isin(master_customer_ids)]
    if not orphaned_records.empty:
        logging.warning(f"Found {len(orphaned_records)} orphaned records (Invalid Customer ID).")
        # Save orphans for manual review
        orphaned_records.to_csv('orphaned_records_review.csv', index=False)
        # Drop from main dataset
        df = df[df['customer_id'].isin(master_customer_ids)]
        
    # 3. Value Validation (Amounts cannot be negative in this ledger)
    negative_values = df[df['total_amount'] < 0]
    if not negative_values.empty:
        logging.warning(f"Found {len(negative_values)} records with negative amounts. Converting to absolute.")
        df.loc[df['total_amount'] < 0, 'total_amount'] = df['total_amount'].abs()
        
    final_count = len(df)
    logging.info(f"Validation complete. Retained {final_count} out of {initial_count} records.")
    
    return df

if __name__ == "__main__":
    # Mock usage for the portfolio repository
    print("Starting ERP Data Migration Validation...")
    
    # In a real scenario, master_customer_ids would be queried from the Oracle DB
    mock_master_ids = {1001, 1002, 1003, 1004, 1005}
    
    # df_raw = load_data('legacy_sales_export.csv')
    # df_clean = validate_and_clean(df_raw, mock_master_ids)
    # df_clean.to_csv('cleaned_sales_ready_for_import.csv', index=False)
    
    print("Pipeline execution simulated successfully. Check migration_validation.log for details.")
