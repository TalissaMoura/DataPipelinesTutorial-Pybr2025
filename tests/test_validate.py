import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from coffee_sales_pipeline.src.pipeline.validate import validate_data

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "coffee_name": ["Latte", "Espresso"],
        "hour_of_day": [10, 15],
        "cash_type": ["cash", "card"],
        "money": [12.5, 8.0],
        "Date": ["2025-10-23", "2025-10-23"],
    })


@patch("pipeline.validate.gx.get_context")
def test_validate_data_success(mock_get_context, tmp_path, sample_dataframe):
    """Testa se a função retorna o DataFrame quando a validação é bem-sucedida."""

    # 🔹 Cria um contexto e toda a hierarquia de mocks usados no código
    mock_context = MagicMock()
    mock_get_context.return_value = mock_context

    # Cria mocks encadeados para data_sources e batch
    mock_data_source = MagicMock()
    mock_data_asset = MagicMock()
    mock_batch_definition = MagicMock()
    mock_batch = sample_dataframe.copy()

    # Configura o comportamento esperado dos mocks
    mock_context.data_sources.add_pandas_filesystem.return_value = mock_data_source
    mock_data_source.add_csv_asset.return_value = mock_data_asset
    mock_context.data_sources.get.return_value.get_asset.return_value = mock_data_asset
    mock_data_asset.add_batch_definition_path.return_value = mock_batch_definition
    mock_batch_definition.get_batch.return_value = mock_batch

    # Mock suite e validator
    mock_suite = MagicMock()
    mock_context.suites.add.return_value = mock_suite
    mock_validator = MagicMock()
    mock_context.get_validator.return_value = mock_validator

    # Simula validação bem-sucedida
    mock_validator.validate.return_value.success = True

    # ✅ Chama a função
    result = validate_data(str(tmp_path), sample_dataframe)

    # Valida o retorno
    pd.testing.assert_frame_equal(result, sample_dataframe)

    # Verifica se expectativas foram chamadas
    mock_validator.expect_column_to_exist.assert_called_with("coffee_name")
    mock_validator.expect_column_values_to_be_between.assert_any_call("hour_of_day", min_value=0, max_value=23)
    mock_validator.expect_column_values_to_be_in_set.assert_any_call("cash_type", ["cash", "card"])


@patch("pipeline.validate.gx.get_context")
def test_validate_data_failure(mock_get_context, tmp_path, sample_dataframe):
    """Testa se a função lança erro quando a validação falha."""

    mock_context = MagicMock()
    mock_get_context.return_value = mock_context

    mock_data_source = MagicMock()
    mock_data_asset = MagicMock()
    mock_batch_definition = MagicMock()
    mock_batch = sample_dataframe.copy()

    mock_context.data_sources.add_pandas_filesystem.return_value = mock_data_source
    mock_data_source.add_csv_asset.return_value = mock_data_asset
    mock_context.data_sources.get.return_value.get_asset.return_value = mock_data_asset
    mock_data_asset.add_batch_definition_path.return_value = mock_batch_definition
    mock_batch_definition.get_batch.return_value = mock_batch

    mock_suite = MagicMock()
    mock_context.suites.add.return_value = mock_suite
    mock_validator = MagicMock()
    mock_context.get_validator.return_value = mock_validator

    # ❌ Validação falha
    mock_validator.validate.return_value.success = False

    with pytest.raises(ValueError, match="Validação falhou"):
        validate_data(str(tmp_path), sample_dataframe)