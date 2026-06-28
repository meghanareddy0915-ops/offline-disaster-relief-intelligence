import pandas as pd

def process_file(uploaded_file):
    file_name = uploaded_file.name

    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        return df.head()

    elif file_name.endswith(".json"):
        import json
        data = json.load(uploaded_file)
        return data

    else:
        return uploaded_file.read().decode("utf-8")


def process_text(text):
    return text.strip()