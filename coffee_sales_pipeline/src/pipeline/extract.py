import pandas as pd

def extract_data(
    file_path: str, 
    start_datetime: str = None, 
    end_datetime: str = None, 
    output_path: str = None
) -> pd.DataFrame:
    """
    Lê o dataset bruto de vendas de café.
    Se start_datetime e end_datetime forem fornecidos (formato 'YYYY-MM-DD HH:MM:SS'), 
    retorna apenas os registros nesse intervalo.
    Se output_path for fornecido, salva o DataFrame filtrado em CSV.
    """
    print("Extraindo dados de:", file_path)
    df = pd.read_csv(file_path)
    print(f"{len(df)} registros carregados.")

    # Combina Date e Time em datetime
    df["event_timestamp"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors="coerce")

    # Filtra por intervalo de datetime se fornecido
    if start_datetime and end_datetime:
        start_dt = pd.to_datetime(start_datetime)
        end_dt = pd.to_datetime(end_datetime)
        df = df[(df["event_timestamp"] >= start_dt) & (df["event_timestamp"] <= end_dt)]
        print(f"{len(df)} registros encontrados entre {start_datetime} e {end_datetime}.")

    # Salva em CSV se output_path for fornecido
    if output_path:
        # Garante que a pasta exista
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        df.to_csv(output_path, index=False)
        print(f"Arquivo CSV filtrado salvo em: {output_path}")

    return df
