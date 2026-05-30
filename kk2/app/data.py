import pandas as pd
import io

DATA = None

def load_csv(file_bytes):
    global DATA

    df = pd.read_csv(io.StringIO(file_bytes.decode("utf-8")))

    DATA = df

    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict()
    }


def get_stats():
    if DATA is None:
        return None

    return DATA.describe().to_dict()