# csv-to-labes

## System requirements
Configure wsl2 ubuntu. You may find instructions at [this](https://learn.microsoft.com/en-us/windows/wsl/install-manual) link.

At the wsl2 follow the next steps.
- Install library to generate png from html
    ```bash
    sudo apt-get -y install wkhtmltopdf
    ```
- Install python3 venv
    ```bash
    sudo apt-get -y install python3-venv
    ```
- Download the code from github
- Go to folder and instatiate the `.env`. This is performed once.
    ``` bash
    cd csv-to-labels
    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
    ```
- Run the `csv_to_labels.py` script
    ``` bash
    python3 csv_to_labels.py
    ```

