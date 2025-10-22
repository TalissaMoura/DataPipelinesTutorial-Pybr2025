import pytest
from coffee_sales_pipeline.src.data.read_coffee_sales import read_coffee_sales_data
import pandas as pd

@pytest.fixture
def sample_data():
    df = read_coffee_sales_data()
    return df

def test_dataframe_hours(sample_data):
    df = sample_data
    assert "hour_of_day" in df.columns, "'hour' column should be present in the DataFrame"
    assert df['hour_of_day'].between(0, 23).all(), "'hour' values should be between 0 and 23"
