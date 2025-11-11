#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Installing requirements..."
pip install -r ./src/requirements.txt

echo "[2/3] Download raw collision data..."
python ./src/import_collisions.py

echo ""
echo "[3/3] Clean and validate data..."
python ./src/clean_dataframe.py

echo ""
#TODO "Add the rest of the pipeline here"
echo "=== Pipeline Complete ==="
