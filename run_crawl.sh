#! /bin/bash
while IFS="," read -r name full_url highlight_url
do
    python3 crawl.py --url highlight_url --output_dir {YOUR_OUTPUT_DIR} --filename name
    python3 crawl.py --url full_url --output_dir {YOUR_OUTPUT_DIR} --filename name
done < data.csv