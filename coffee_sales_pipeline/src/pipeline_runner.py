""" Objetivo: executar o pipeline de vendas de café, 
              gerar os dados que vão ser recebidos no dashboard: 
                - even_timestap, 
                - quantidade de vendas gerais e por tipo de café, 
                - média de vendas de café por hora (quantidade e valor)

"""
from pipeline.extract import extract_data
from pipeline.validate import validate_data
from pipeline.transform import transform_data
from pipeline.load import load_data
import os

if __name__ == "__main__":
    print("Iniciando pipeline de vendas da cafeteria...")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "src/data")
    raw_path = os.path.join(DATA_DIR, "raw", "coffee_sales_data.csv")
    output_path = os.path.join(DATA_DIR, "processed", "coffee_sales_summary.csv")

    # Etapas
    df_raw = extract_data(raw_path)
    df_valid = validate_data(DATA_DIR, df_raw)  # Usa Great Expectations
    df_transformed = transform_data(df_valid)
    load_data(df_transformed, output_path)

    print("Pipeline finalizado com sucesso!")

