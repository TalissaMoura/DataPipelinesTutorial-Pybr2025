import great_expectations as gx
import pandas as pd
import os

def validate_data(source_folder: str, df_extractor: pd.DataFrame) -> pd.DataFrame:
    """Valida o dataset de vendas usando Great Expectations."""
    print("Validando dados com Great Expectations...")

    context = gx.get_context()

    # Define the Data Source's parameters:
    # This path is relative to the base_directory of the Data Context.
    source_folder = source_folder
    data_source_name = "raw"

    # Create the Data Source:
    data_source = context.data_sources.add_pandas_filesystem(
        name=data_source_name, base_directory=source_folder
    )
    data_asset_name = "coffee_sales_data_asset"
    # Add a Data Asset to the Data Source:
    data_asset = data_source.add_csv_asset(name=data_asset_name)

    # Define a Batch Definition
    file_data_asset = context.data_sources.get(data_source_name).get_asset(data_asset_name)
    batch_definition_name = "my_batch_definition"
    batch_definition_path = "raw/coffee_sales_data.csv"
    batch_definition = file_data_asset.add_batch_definition_path(
        name=batch_definition_name, path=batch_definition_path
    )

    batch = batch_definition.get_batch()
    print(batch.head())

    suite_name = "coffee_sales_expectations"
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))

    validator = context.get_validator(
        batch=batch,
        expectation_suite_name=suite_name,
    )

    # A coluna deve existir
    validator.expect_column_to_exist("coffee_name")

    # A coluna 'hour_of_day' deve conter apenas valores entre 0 e 23
    validator.expect_column_values_to_be_between("hour_of_day", min_value=0, max_value=23)

    # A coluna 'cash_type' deve conter apenas valores de uma lista conhecida
    validator.expect_column_values_to_be_in_set("cash_type", ["cash", "card"])

    # A coluna 'money' não deve ter valores nulos e deve ser positiva
    validator.expect_column_values_to_not_be_null("money")
    validator.expect_column_values_to_be_between("money", min_value=0)

    # A coluna 'Date' deve ter formato de data válido
    validator.expect_column_values_to_match_strftime_format("Date", "%Y-%m-%d")

    if validator.validate().success:
        print("Validação concluída com sucesso!")
        return df_extractor
    else:
        raise ValueError("Validação falhou. Verifique os dados de entrada.")
# validate_data()