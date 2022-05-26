#! /bin/bash
while IFS="," read -r name full highlight
do
    # echo "$name $full $highlight"
    highlight_name=$name"_highlight.mp4"
    full_name=$name"_full.mp4"
    python3 crawl_soccer_highlight.py --url $highlight --output_dir {YOUR_OUTPUT_DIR} --filename $highlight_name
    python3 crawl_soccer_full.py --url $full --output_dir {YOUR_OUTPUT_DIR} --filename $full_name
done < /Users/jwhwang/video_downloader/sbs.csv