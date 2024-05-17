### List all files aws s3 version
```
aws s3 ls s3://it.neratech.feem/OnSSET/v2/
```
### Download XLSX output aws s3 version
```
PROJECT_PATH="$HOME/lab/python/feem/feem-onnset-tools"
DATA_PATH="${PROJECT_PATH}/data"
mkdir -pv "${DATA_PATH}"
aws s3 cp s3://it.neratech.feem/OnSSET/OnSSET_results.xlsx "${DATA_PATH}/"

aws s3 cp s3://it.neratech.feem/OnSSET/v2/ke-2-0_0_0_0_0_0.csv "${DATA_PATH}/"
aws s3 cp s3://it.neratech.feem/OnSSET/v2/ke-2-0_0_0_0_0_1.csv "${DATA_PATH}/"
aws s3 sync s3://it.neratech.feem/OnSSET/v2/ "${DATA_PATH}/csv/"
```

# steps
```
python3.12 -m venv env
source env/bin/activate (for Linux)
.\env\Scripts\activate.bat (for Windows)
(env) python -m pip install -U pip setuptools wheel
(env) python -m pip install -r requirements.txt
(env) cd src
(env) python main.py --help 
```

# run
```
# prepare .env file with following property

CURRENT_YEARS='[2025,2030]'
DELETE_TEMPORARY_FILE=0|1
LOCAL_WORKING_FOLDER=...
LOG_LEVEL=DEBUG|INFO|WARNING

(env) python main.py parse-csv-files
```