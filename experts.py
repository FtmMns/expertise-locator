import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path, encoding='utf-8', dtype=str)  
    df.columns = df.columns.str.strip()  # Remove spaces from column names
    return df

def search_experts(df, first_name=None, last_name=None, department=None, expert_keyword=None, any_keyword=None):
    filtered_df = df.copy()
    
    # Filter by First Name
    if first_name:
        filtered_df = filtered_df[filtered_df['First Name'].str.contains(first_name, case=False, na=False)]
    
    # Filter by Last Name
    if last_name:
        filtered_df = filtered_df[filtered_df['Last Name'].str.contains(last_name, case=False, na=False)]

    if department:
        filtered_df = filtered_df[filtered_df['Department'].str.contains(department, case=False, na=False)]

    
    # Filter by Expert Keyword (Search in all columns EXCEPT "First Name" and "Last Name")
    if expert_keyword:
        cols_to_search = [col for col in filtered_df.columns if col not in ["First Name", "Last Name"]]
        filtered_df = filtered_df[filtered_df[cols_to_search].apply(lambda row: row.astype(str).str.contains(expert_keyword, case=False, na=False).any(), axis=1)]
    
    # Filter by Any Keyword (Search in ALL columns)
    if any_keyword:
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(any_keyword, case=False, na=False).any(), axis=1)]
    
    return filtered_df

# Load the dataset
file_path = "Cleaned_Expert_Dataset.csv"
df = load_data(file_path)

# Streamlit UI
st.title("Expert Locator System")

first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
department=st.text_input("Department")
expert_keyword = st.text_input("Search Expertise")
any_keyword = st.text_input("Search Any Keyword (searches in all columns)")

if st.button("Search", key="search_button"):
    results = search_experts(df, first_name, last_name, department,expert_keyword, any_keyword)
    if results.empty:
        st.warning("No user found!")
    else:
        st.write(results)
