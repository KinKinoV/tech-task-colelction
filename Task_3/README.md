# How to use

To use script I developed, you have to follow these instructions:
1. Install all requirements from `requirements.txt` using this command:
```bash
pip install -r requirements.txt
```
2. Go to the script and find line 138 where `raw_data` variable is declared
3. Edit parameters passed to the `make_request()` function to fit your needs
4. Execute the script using `python3 main.py` command

Results of execution of the script should be a `processed.json` file in the same folder where you executed the script and window with line chart that will show temperature dynamic over days that were requested from the API.

# Script logic

This script works in such way:
1. Firstly `raw_data` variable gets output of the `make_request()` function that is immediatly converted to python `dict`. Requests  are made to the [Open-Meteo](https://open-meteo.com/) API with parameters declared by user when calling the `make_request()` function. All of the parameters used are listed in the Open-Meteo API documentation.
2. Then data is processed in the `process_data()` function, that counts average temperature over days listed in the received data. Additionally it stores all other important information from request's response.
3. Finally, processed data is converted to `JSON` format and is saved locally in the same directory where script was executed. After data is saved script draws and shows line graph reflecting stored data.