import pandas as pd

# Define column headers
columns = [
    "version", "account-id", "interface-id", "srcaddr", "dstaddr", 
    "srcport", "dstport", "protocol", "packets", "bytes", 
    "start", "end", "action", "log-status"
]

# Read the file into a DataFrame, assuming it's tab-separated
file_path = "203918869513_vpcflowlogs_us-east-1_fl-0dcd7118d3d79b1fd_20241028T1715Z_20cf06cd.log"
df = pd.read_csv(file_path, sep=" ", names=columns, skipinitialspace=True)

# Display the DataFrame with improved readability
pd.set_option("display.max_rows", None)  # Remove row limit
pd.set_option("display.max_columns", None)  # Remove column limit
pd.set_option("display.width", 1000)  # Increase display width
pd.set_option("display.colheader_justify", "center")  # Center column headers

print(df)

# Save to CSV or Excel
# df.to_csv("formatted_output.csv", index=False)
df.to_excel("formatted_output.xlsx", index=False)
