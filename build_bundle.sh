#!/bin/bash

set -e

echo "=========================================="
echo " Building FINAL PROJECT BUNDLE..."
echo "=========================================="

PROJECT="credit-card-fraud-detection"
BUNDLE_DIR="bundle_$PROJECT"

# Clean old bundle
rm -rf $BUNDLE_DIR
mkdir $BUNDLE_DIR

echo "[1] Copying project files..."
cp -r app src model data frontend notebook tests $BUNDLE_DIR/
cp Dockerfile requirements.txt README.md $BUNDLE_DIR/

echo "[2] Removing unnecessary Python cache..."
find $BUNDLE_DIR -type d -name "__pycache__" -exec rm -rf {} +

echo "[3] Creating ZIP..."
zip -r "${PROJECT}_bundle.zip" $BUNDLE_DIR >/dev/null

echo "DONE!"
echo "Created: ${PROJECT}_bundle.zip"
echo "Bundle Folder: ${BUNDLE_DIR}/"
