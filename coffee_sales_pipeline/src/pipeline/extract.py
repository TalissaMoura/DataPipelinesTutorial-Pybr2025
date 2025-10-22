import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    """Lê o dataset bruto de vendas de café."""
    print("Extraindo dados de:", file_path)
    df = pd.read_csv(file_path)
    print(f"{len(df)} registros carregados.")
    return df
# extract_data("../data/raw/coffee_sales_data.csv")