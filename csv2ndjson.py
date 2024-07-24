import pandas as pd
import os
import csv
import json

# Load and pre-process the CSV file
csv_file_path = 'laptop_price.csv'
processed_file_path = 'processed_file.csv'

# Replace double quotes with 'in' in the file
with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as file:
    content = file.read().replace('"', 'in')

# Save the processed content to a new file
with open(processed_file_path, 'w', encoding='utf-8') as file:
    file.write(content)

# Try reading the processed CSV file with different encodings
encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
for encoding in encodings:
    try:
        df = pd.read_csv(
            processed_file_path, 
            encoding=encoding, 
            quoting=csv.QUOTE_NONE, 
            on_bad_lines='skip'
        )
        break
    except (UnicodeDecodeError, pd.errors.ParserError):
        continue
else:
    raise UnicodeDecodeError("All tried encodings failed to decode the file.")

# Generate JSON filename based on CSV filename
csv_filename = os.path.basename(csv_file_path)
json_filename = f"{os.path.splitext(csv_filename)[0]}_ndjson.json"
ndjson_file_path = os.path.join(os.path.dirname(csv_file_path), json_filename)

# Convert DataFrame to newline-delimited JSON with properly quoted keys
with open(ndjson_file_path, 'w', encoding='utf-8') as file:
    for record in df.to_dict(orient='records'):
        json_record = json.dumps(record, ensure_ascii=False)  # Ensure proper JSON formatting
        file.write(f"{json_record}\n")

print(f"Newline-delimited JSON file saved as: {ndjson_file_path}")
