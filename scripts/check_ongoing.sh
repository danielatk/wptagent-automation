#!/bin/bash

ongoing_file_path="$1"
check_interval=10  # in seconds
timeout=300        # 5 minutes in seconds

flag_file="/tmp/flag"

while true; do
    file_content=$(cat "$ongoing_file_path")

    if [ "$file_content" = "0" ]; then
        rm "$flag_file" 2>/dev/null
    else
        if [ -e "$flag_file" ]; then
            start_time=$(cat "$flag_file")
            current_time=$(date +%s)
            elapsed_time=$((current_time - start_time))

            if [ $elapsed_time -ge $timeout ]; then
                echo "Timeout reached. Changing file content to 0."
                echo "0" > "$ongoing_file_path"
                rm "$flag_file"
            fi
        else
            echo $(date +%s) > "$flag_file"
        fi

        sleep $check_interval  # Wait for the specified interval
    fi

    sleep $check_interval  # Wait for the specified interval
done