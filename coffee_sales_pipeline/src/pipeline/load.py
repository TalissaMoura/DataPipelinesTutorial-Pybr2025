import os
import pandas as pd

def load_data(df: pd.DataFrame, output_path: str):
    """Salva o resultado processado."""
    print("Salvando dados processados em:", output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print("Dados salvos com sucesso!")
