import pandas as pd
import os

# Default data path assuming app/utils/data_loader.py structure
DEFAULT_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'PAC_Performance_Template.xlsx')

def load_all_sheets(file_path=DEFAULT_DATA_PATH):
    """
    Reads an Excel file and loads all its sheets automatically with specific cleaning.
    """
    if not os.path.exists(file_path):
        return {}
    
    try:
        # Load sheets with specific header configs to match layout
        # default header is 0
        excel_data = pd.read_excel(file_path, sheet_name=None, header=None)
        clean_data = {}
        
        for sheet_name, raw_df in excel_data.items():
            df = raw_df.copy()
            # Clean completely empty rows and columns
            df.dropna(how='all', inplace=True)
            df.dropna(how='all', axis=1, inplace=True)
            
            # Apply header skipping logic depending on known templates
            if sheet_name in ["Closures Summary", "Onboarding Impact", "Behavioral Contribution"]:
                # Headers are generally on row index 2 (the 3rd row)
                # Let's find the first row that is quite full to be the header
                # Or just hardcode for these known ones
                if len(df) > 2:
                    new_header = df.iloc[2]
                    df = df[3:]
                    df.columns = new_header
                    
            elif sheet_name == "Leaves":
                # User provided specific leaves text, might just have a standard header or mixed
                # Find first row with 'Leave Type'
                header_idx = df[df.apply(lambda r: r.astype(str).str.contains("Leave Type").any(), axis=1)].index
                if len(header_idx) > 0:
                    idx = header_idx[0]
                    new_header = df.loc[idx]
                    df = df.loc[idx+1:]
                    df.columns = new_header
            
            # Also handle if Candidate Closures is just header=0
            elif sheet_name == "Candidate Closures":
                if len(df) > 0:
                    new_header = df.iloc[0]
                    df = df[1:]
                    df.columns = new_header
            
            # Reset index and strip col names
            df.reset_index(drop=True, inplace=True)
            if not df.empty and df.columns.nlevels == 1:
                df.columns = [str(col).strip() if pd.notna(col) else f"Unnamed_{i}" for i, col in enumerate(df.columns)]
                
            clean_data[sheet_name] = df
            
        return clean_data
    except Exception as e:
        print(f"Error loading Excel file from {file_path}: {str(e)}")
        return {}

def get_sheet_data(sheet_name, data_dict=None):
    """
    Helper to get a specific sheet's dataframe from the loaded data dictionary.
    """
    if data_dict is None:
        data_dict = load_all_sheets()
        
    return data_dict.get(sheet_name, pd.DataFrame())

def get_sheet_names(data_dict=None):
    """
    Return a list of all available sheet names.
    """
    if data_dict is None:
        data_dict = load_all_sheets()
        
    return list(data_dict.keys())
