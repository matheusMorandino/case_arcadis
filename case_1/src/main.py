import os
import camelot
from pypdf import PdfReader

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def separate_tables(original_dataframe):
    # Identify empty rows to split the tables
    empty_rows = original_dataframe.isnull().all(axis=1)

    # Find the indices where the tables are split
    split_indices = empty_rows[empty_rows].index

    # Initialize a list to store separate DataFrames
    separated_tables = []

    # Initialize start index for the first table
    start_idx = 0

    # Iterate through split indices to extract individual tables
    for split_idx in split_indices:
        # Extract the table from the original DataFrame
        table = original_dataframe.iloc[start_idx:split_idx]

        # Check if the table has any non-null values (to handle consecutive empty rows)
        if not table.isnull().all().all():
            separated_tables.append(table)

        # Update the start index for the next table
        start_idx = split_idx + 1

    # Add the last table if there are non-null values
    last_table = original_dataframe.iloc[start_idx:]
    if not last_table.isnull().all().all():
        separated_tables.append(last_table)

    return separated_tables


pdf_path = os.path.join(ROOT_DIR, "input\\Material_Case_Ex1.pdf")

tables = camelot.read_pdf(pdf_path, flavor='stream', pages='all')

# Assuming the data is in the first table
dfs = tables[0].df

# Display the DataFrame
separated_tables_list = separate_tables(dfs)

print(separated_tables_list)