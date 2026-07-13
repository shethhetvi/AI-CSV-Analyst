import os
import pandas as pd

def save_and_load_csv(uploaded_file) -> pd.DataFrame:
    """
    Saves the uploaded Streamlit file to the uploads/ directory
    and returns a pandas DataFrame.
    """
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        
    file_path = os.path.join("uploads", uploaded_file.name)
    
    # Save file physically
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    # Read into pandas
    df = pd.read_csv(file_path)
    return df
