from pipeline.extract import extract_data
from pipeline.validate import validate_data
from pipeline.transform import transform_data
from pipeline.load import load_data
import os

def run_pipeline(start_datetime: str, end_datetime: str):
    """Executa todo o pipeline de vendas de café para um intervalo de data e hora específico."""
    print("☕ Iniciando pipeline de vendas da cafeteria...")

    # Definindo caminhos
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "src/data")
    raw_path = os.path.join(DATA_DIR, "raw", "coffee_sales_data.csv")
    filtered_output_path = os.path.join(DATA_DIR, "filter", "coffee_sales_filter.csv")
    processed_output_path = os.path.join(DATA_DIR, "processed", "coffee_sales_summary.csv")

    # Etapas do pipeline
    df_raw = extract_data(raw_path, start_datetime, end_datetime, filtered_output_path)
    df_valid = validate_data(DATA_DIR, df_raw)  # Usa Great Expectations
    df_transformed = transform_data(df_valid)
    load_data(df_transformed, processed_output_path)

    print("✅ Pipeline finalizado com sucesso!")

# Exemplo de execução
if __name__ == "__main__":
    run_pipeline(start_datetime="2024-03-01 19:00:00", end_datetime="2024-03-01 19:59:00")
