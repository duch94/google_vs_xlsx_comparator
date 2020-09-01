# How to run 
Run `main.py` with python 3.7 and above. Use flag `--help` to learn how to use it.
To run this script you need credentials.json to access google sheet. 

You can read more info about google API credentials at https://console.cloud.google.com/apis/credentials.

# How to build
Run `poetry build` (you need to install poetry first with command `pip install poetry`). 
After that you will have sdist and wheel packages in `dist` directory.

File `setup.py` is inside of sdist package (`*.tar.gz`).

# How to install dependencies 
Run `poetry install`.

# How to test
Run `python -m unittest`.
