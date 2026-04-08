#!/bin/bash

# Download AnimeGameData TextMap archive and extract to raw/langs
URL="https://gitlab.com/Dimbreath/AnimeGameData/-/archive/master/AnimeGameData-master.tar?ref_type=heads&path=TextMap"
OUTPUT_DIR="raw/langs"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Download the tar file
echo "Downloading from $URL..."
curl -L -o temp.tar "$URL"

# Extract to the output directory
echo "Extracting..."
tar -xf temp.tar

# Clean up temporary file
rm -f temp.tar

# move extracted files to the output directory
echo "Moving files to $OUTPUT_DIR..."
mv AnimeGameData-master-TextMap/TextMap/* "$OUTPUT_DIR/"

echo "Done!"
