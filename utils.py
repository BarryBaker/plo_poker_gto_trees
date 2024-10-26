import pandas as pd

gto_path = "solved/"


def merge_csvs(file_paths):

    # Initialize an empty list to store each CSV as a DataFrame
    dfs = []

    # Iterate through each file path
    for file_path in file_paths:

        # Read the CSV file into a DataFrame
        df = pd.read_csv(gto_path + file_path)

        # Get the file name without the extension to use in the column name
        file_name = file_path.replace(".csv", "").split("_")[-1]

        # Rename the weight column to include the CSV file name
        df = df.rename(columns={"weight": file_name})

        # Append to the list of DataFrames
        dfs.append(df)

    # Merge all DataFrames on the 'combo' column, using an outer join to include all combos
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on="combo", how="outer")

    # Fill missing values in weight columns with 0
    weight_columns = [col for col in merged_df.columns if col != "combo"]
    merged_df[weight_columns] = merged_df[weight_columns].fillna(0)

    merged_df = merged_df.set_index("combo")

    return merged_df
