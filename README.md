# englex-csv

This is a script for exporting all your words from Englex personal dictionaries to a CSV file.

## Installing dependencies

```shell
# Creating a virtual environment.
python3 -m venv venv
source venv/bin/activate

# Installing dependencies.
pip install -r requirements.txt
```

## Running the script

You need to specify necessary environment variables:

| Variable name        | Description          |
|----------------------|----------------------|
| ENGLEX_USER_EMAIL    | User's email address |
| ENGLEX_USER_PASSWORD | User's password      |

Next you can run the `main.py` script, it will create `englex.csv` file with your data.

You can also specify an alternative export path in the script arguments.

```shell
# Exporting the environment variables.
export ENGLEX_USER_EMAIL=student@example.com
export ENGLEX_USER_PASSWORD=my_secret_password

# Run the script.
python3 main.py
# Or you can...
python3 main.py another/path/to/save/output.csv
```
