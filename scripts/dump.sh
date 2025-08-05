#!/bin/bash
rg --files "$@" | while read -r file; do
    size=$(stat -c %s "${file}")
    ext="${file##*.}"

    printf "%6s | %s\n" "${size}" "${file}" >&2
    echo "**${file}**"
    echo "\`\`\`${ext}"
    cat "${file}"
    echo
    echo "\`\`\`"
done