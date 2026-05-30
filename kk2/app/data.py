import pandas as pd
import io
from typing import Optional, Dict, Any

DATA = None


def load_csv(file_bytes: bytes) -> Dict:
    global DATA
    df = pd.read_csv(io.StringIO(file_bytes.decode("utf-8")))
    DATA = df
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
    }


def get_stats() -> Optional[Dict]:
    if DATA is None:
        return None
    return DATA.describe(include="all").fillna("").to_dict()