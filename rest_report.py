import requests
import pandas as pd
import gzip
import zipfile
import os
import re
import io


# ==============================
# CONFIGURATION
# ==============================

url = "http://192.168.1.157:8080/openmrs/ws/rest/v1/kenyaemr/reportRequests/1756/download/csv"

username = "admin"
password = "Admin123"


download_file = "report_download"
csv_file = "report_1753.csv"
excel_file = "report_1753.xlsx"


# ==============================
# DOWNLOAD
# ==============================

print("Downloading report...")

response = requests.get(
    url,
    auth=(username, password),
    timeout=300
)


print("Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    exit()


content = response.content


print("Downloaded bytes:", len(content))


# ==============================
# DETECT COMPRESSION
# ==============================

# ZIP file signature
if content[:2] == b'PK':

    print("ZIP file detected")

    with zipfile.ZipFile(io.BytesIO(content)) as z:

        print("Files inside ZIP:")
        print(z.namelist())

        filename = z.namelist()[0]

        with z.open(filename) as f:

            with open(csv_file, "wb") as out:
                out.write(f.read())


# GZIP signature
elif content[:2] == b'\x1f\x8b':

    print("GZIP file detected")

    with gzip.open(
        io.BytesIO(content),
        "rb"
    ) as f:

        with open(csv_file, "wb") as out:
            out.write(f.read())


else:

    print("Normal CSV detected")

    with open(csv_file, "wb") as f:
        f.write(content)



print("CSV extracted:", csv_file)



# ==============================
# READ CSV
# ==============================

print("Reading CSV...")


df = pd.read_csv(
    csv_file,
    encoding="latin1",
    sep=",",
    engine="python",
    on_bad_lines="skip"
)


print("Rows:", len(df))
print("Columns:", len(df.columns))


print(df.head())



# ==============================
# CLEAN EXCEL CHARACTERS
# ==============================

def clean_text(value):

    if isinstance(value, str):

        return re.sub(
            r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]',
            '',
            value
        )

    return value


df = df.map(clean_text)



# ==============================
# EXPORT
# ==============================

df.to_csv(
    "report_1753_clean.csv",
    index=False,
    encoding="utf-8"
)


df.to_excel(
    excel_file,
    index=False
)


print("Completed successfully")