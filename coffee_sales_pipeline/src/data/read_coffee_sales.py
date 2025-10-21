import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
import pathlib

FILE_PATH = "Coffe_sales.csv"
KAGGLE_DATASET = "navjotkaushal/coffee-sales-dataset"

def read_coffee_sales_data(file_path_to_save:str):
    try:
        df = pd.read_csv(file_path_to_save + "/coffee_sales_data.csv")
        print(f"Dataset loaded from {file_path_to_save}/coffee_sales_data.csv")
    except FileNotFoundError:
        df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        KAGGLE_DATASET,
        FILE_PATH,
        )
        path_to_save = pathlib.Path(file_path_to_save)
        if not path_to_save.exists():
            path_to_save.mkdir(parents=False, exist_ok=True)
        df.to_csv(path_to_save / "coffee_sales_data.csv", index=False)
        print(f"Dataset saved to {path_to_save / 'coffee_sales_data.csv'}")
    return df

if __name__ == "__main__":
    df = read_coffee_sales_data("./raw")
    print(df.head())