## Valuation Details Scraper for AlphaSpread

This tool is designed to scrape valuation details from the AlphaSpread website.

### Setup Instructions:

1. **Environment Setup**: Create a virtual environment and install the required dependencies.

    ```bash
    # Create and activate a virtual environment (optional but recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate.bat

    # Install dependencies
    pip install -r requirements.txt
    ```

2. **Run the Scraper**: Execute the main script.

    ```bash
    python main.py
    ```

3. **Starting from Scratch**: If you're starting from scratch, remove the `processed_stocks_log_` file.

    ```bash
    rm processed_stocks_log_
    ```

4. **Remove Data from MongoDB**: To clear the data stored in MongoDB, run the delete script.

    ```bash
    python delete_data.py
    ```

5. **Run the Scraper Again**: Run the main script once more.

    ```bash
    python main.py
    ```

### Handling Interruptions:

- If the execution is interrupted or stopped, the code will automatically resume from where it left off. It verifies this using the `processed_stocks_log_` file.

### Retrieving Data from MongoDB:

To access the scraped data stored in MongoDB, use the following command:

```bash
python get_data.py
```

The results will be saved in the `stock_data_output` directory.

--- 