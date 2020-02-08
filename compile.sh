#!/bin/bash

# remove any previously generated site
rm -r docs/*
rm -r pages/*

# Collect articles from github
python3 query-github.py

# copy index.md to pages
cp index.md pages

# build archive page
echo "# Projects" >> pages/archive.md
pages=$(ls -r pages/*.md | xargs -n 1 basename)
year=""
for i in $pages; do
    if [ $i = "archive.md" -o $i = "index.md" ]; then
        :
    else
        if [[ $year != ${i:0:4} ]]; then
            year=${i:0:4}
            echo "" >> pages/archive.md
            echo "## $year\n" >> pages/archive.md
            echo "" >> pages/archive.md
        fi
        echo "* [${i%.*}](${i%.*}.html)" >> pages/archive.md
    fi
done

# convert md pages to html
md=$(ls pages/*.md | xargs -n 1 basename)
for i in $md; do
    echo "Converting .... $i"
    pandoc -s pages/$i -o pages/${i%.*}.html --metadata title=" "
done

# compile pages with header and footer
pages=$(ls pages/*.html | xargs -n 1 basename)
for i in $pages; do
    echo "Compiling ..... $i"
    cat head.html > docs/$i
    cat pages/$i >> docs/$i
    cat foot.html >> docs/$i
    echo "Site generated $(date +%Y-%m-%d)" >> docs/$i
done

# move assets
cp media/* docs/
cp *.css docs/
