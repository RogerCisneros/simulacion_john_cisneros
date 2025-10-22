import pandas as pd

def export_results_to_excel(df, path):
    df.to_excel(path, index=False)
