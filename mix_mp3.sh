#!/bin/bash

# Create a list of all mp3 files in the current directory in the desired order
files=($(ls [0-9]*.mp3 | sort -V))

# Create a temporary file to store the list of files
temp_file=$(mktemp)

# Write the list of files to the temporary file
for file in "${files[@]}"; do
  # Use absolute paths to avoid issues with temporary directories
  abs_path=$(realpath "$file")
  echo "file '$abs_path'" >> "$temp_file"
done

# Use the temporary file as input for ffmpeg
current_datetime=$(date +"%Y%m%d_%H%M%S")
output_file="output_${current_datetime}.mp3"
ffmpeg -f concat -safe 0 -i "$temp_file" -c copy "$output_file"
# Remove the temporary file
rm "$temp_file"

echo "Concatenation complete: output.mp3"
