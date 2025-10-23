



# How to run this project 
 1 - Install [uv](https://github.com/astral-sh/uv)
 2 - Run the command inside the coffee_sales_pipeline folder
   ```
        uv sync
   ```
 3 - To activate the venv run:
   ```
     source .venv/bin/activate
   ```
 4 - The project structure is like this:
 
   Inside the `./coffee_sales_pipeline`:
   - src: contains the project files according with their function. 
     - data: contains the modules and functions to handle with the data. Also, in `/raw` directory
     is saved the data we need for the project. You can run the `read_coffee_sales.py` to load the dataset. 
     - pipeline: containes modules to apply the pipeline logic and handle data quality testing.
     - pipeline_runner.py: Aggregates all the logic to run the pipeline, at the end, this is the file that
     generates the treated data for the dashboard.
   - streamlit: contains the modules and functions for the dashboard. To visualize run:
     ```
        uv run streamlit run streamlit_app.py
     ```
   - tests: Contains the test files for the pipeline.