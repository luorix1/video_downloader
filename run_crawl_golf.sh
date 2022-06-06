#! /bin/bash
while IFS="," read -r name highlight full
do
    # echo "$name $highlight $full"
    highlight_name=$name"_highlight.mp4"
    full_name=$name"_full.mp4"
    python3 crawl_golf_highlight.py --url $highlight --output_dir ${YOUR_OUTPUT_DIR} --filename $highlight_name
    python3 crawl_golf_full.py --url $full --id ${YOUR_ID} --pwd ${YOUR_PASSWORD} --output_dir ${YOUR_OUTPUT_DIR} --filename $full_name
done < ./golf.csv