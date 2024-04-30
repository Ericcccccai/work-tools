import pandas as pd
from collections import defaultdict

# The data string as provided in your question (truncated here for demonstration)
data_string = """
Final Results:
Results for 2023-11-13:
  Building Interior - Level 1: 227 drawings
  Building Interior - Level 2: 194 drawings
  Building Interior - Roof: 26 drawings
  Building Interior - Level 3: 249 drawings
  Building Interior - Level 4: 272 drawings
  Total images: 968
Results for 2023-11-20:
  Building Interior - Level 1: 79 drawings
  Building Interior - Level 3: 166 drawings
  Building Interior - Level 4: 133 drawings
  Total images: 378
Results for 2023-12-01:
  Building Interior - Roof: 17 drawings
  Building Interior - Level 4: 225 drawings
  Building Interior - Level 3: 67 drawings
  Building Interior - Level 2: 201 drawings
  Building Interior - Level 1: 153 drawings
  Total images: 663
Results for 2023-12-08:
  Building Interior - Level 1: 140 drawings
  Building Interior - Level 2: 303 drawings
  Building Interior - Level 3: 329 drawings
  Building Interior - Level 4: 163 drawings
  Total images: 935
Results for 2023-12-15:
  Building Interior - Level 4: 206 drawings
  Building Interior - Level 1: 48 drawings
  Building Interior - Level 2: 138 drawings
  Building Interior - Roof: 24 drawings
  Building Interior - Level 3: 186 drawings
  Total images: 602
Results for 20231013:
  Building Interior - Level 4: 1770 drawings
  Building Interior - Level 1: 229 drawings
  Building Interior - Level 3: 200 drawings
  Total images: 2199
Results for 20231020:
  Building Interior - Level 4: 194 drawings
  Total images: 194
Results for 20231027:
  Building Interior - Level 4: 161 drawings
  Total images: 161
Results for 20231106:
  Building Interior - Level 4: 117 drawings
  Total images: 117
Results for 2024-01-05:
  Building Interior - Roof: 5 drawings
  Building Interior - Level 4: 126 drawings
  Building Interior - Level 3: 138 drawings
  Building Interior - Level 2: 311 drawings
  Building Interior - Level 1: 109 drawings
  Total images: 689
Results for 2024-01-18:
  Building Interior - Level 3: 382 drawings
  Building Interior - Roof: 15 drawings
  Building Interior - Level 4: 386 drawings
  Total images: 783
Results for 2024-01-26:
  Building Interior - Level 3: 88 drawings
  Building Interior - Level 4: 103 drawings
  Total images: 191
Results for 2024-01-29:
  Building Interior - Roof: 43 drawings
  Total images: 43
Results for 20240112:
  Building Interior - Level 3: 389 drawings
  Building Interior - Level 2: 222 drawings
  Building Interior - Roof: 11 drawings
  Building Interior - Level 4: 346 drawings
  Building Interior - Level 1: 72 drawings
  Total images: 1040
Results for 20240119:
  Building Interior - Level 2: 65 drawings
  Building Interior - Level 1: 248 drawings
  Building Interior - Level 4: 329 drawings
  Total images: 642
Results for 20240126:
  Building Interior - Level 3: 115 drawings
  Building Interior - Level 4: 232 drawings
  Total images: 347
Results for 20240129:
  Building Interior - Level 2: 204 drawings
  Building Interior - Level 3: 396 drawings
  Total images: 530
Results for 20240201:
  Building Interior - Level 1: 259 drawings
  Building Interior - Level 3: 409 drawings
  Total images: 530
Results for 20240202:
  Building Interior - Level 1: 61 drawings
  Building Interior - Level 4: 363 drawings
  Total images: 424
Results for 20240208:
  Building Interior - Level 3: 472 drawings
  Building Interior - Level 1: 236 drawings
  Total images: 708
Results for 20240209:
  Building Interior - Level 1: 269 drawings
  Building Interior - Level 4: 188 drawings
  Total images: 457
Results for 20240215:
  Building Interior - Level 1: 172 drawings
  Building Interior - Level 3: 71 drawings
  Total images: 243
Results for 20240216:
  Building Interior - Level 4: 137 drawings
  Building Interior - Level 2: 20 drawings
  Total images: 157
Results for 20240222:
  Building Interior - Level 1: 250 drawings
  Building Interior - Level 2: 277 drawings
  Building Interior - Level 3: 294 drawings
  Total images: 821
Results for 20240227:
  Building Interior - Level 4: 151 drawings
  Total images: 151
Results for 20240229:
  Building Interior - Level 3: 135 drawings
  Building Interior - Level 1: 253 drawings
  Building Interior - Level 2: 164 drawings
  Total images: 552
Results for 20240301:
  Building Interior - Level 4: 215 drawings
  Total images: 215
Results for 20240307:
  Building Interior - Level 1: 276 drawings
  Building Interior - Level 2: 259 drawings
  Building Interior - Level 3: 343 drawings
  Total images: 878
Results for 20240308:
  Building Interior - Level 4: 319 drawings
  Total images: 319
Results for 20240314:
  Building Interior - Level 1: 211 drawings
  Building Interior - Level 3: 204 drawings
  Total images: 415
Results for 20240315:
  Building Interior - Level 4: 330 drawings
  Total images: 330
Results for 20240318:
  Building Interior - Level 2: 217 drawings
  Building Interior - Roof: 19 drawings
  Total images: 236
Results for 20240321:
  Building Interior - Level 1: 288 drawings
  Building Interior - Level 3: 212 drawings
  Total images: 404
Results for 20240322:
  Building Interior - Level 4: 270 drawings
  Building Interior - Level 2: 180 drawings
  Total images: 404
Results for 20240328:
  Building Interior - Level 4: 8 drawings
  Total images: 8
Results for 20240329:
  Building Interior - Level 3: 313 drawings
  Building Interior - Level 2: 125 drawings
  Building Interior - Level 1: 275 drawings
  Total images: 713
"""

# Parsing the data
results = defaultdict(dict)
current_tag = None
for line in data_string.split('\n'):
    line = line.strip()
    if line.startswith('Results for'):
        current_tag = line.split(' ')[2].strip(':')
    elif line.startswith('Building Interior'):
        parts = line.split(':')
        level = parts[0].strip()
        count = int(parts[1].split()[0])
        results[current_tag][level] = count
    elif line.startswith('Total images'):
        count = int(line.split(':')[1].split()[0].strip())
        results[current_tag]['Total images'] = count

columns = ['Date', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Roof', 'Total Images']
data = {col: [] for col in columns}

for date, info in results.items():
    data['Date'].append(date)
    for level in ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Roof']:
        data[level].append(info.get(f'Building Interior - {level}', 0))
    data['Total Images'].append(info.get('Total images', 0))

df = pd.DataFrame(data)

# Save DataFrame to Excel
excel_file_path = 'Building_Interior_Results.xlsx'  # Define the file path
df.to_excel(excel_file_path, index=False, engine='openpyxl')

print(f"Data has been successfully saved to {excel_file_path}")
