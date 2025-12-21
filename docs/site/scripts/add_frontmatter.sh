#!/bin/bash
# Usage: ./add_frontmatter.sh "Title" "template.html" [weight]

TITLE="$1"
TEMPLATE="$2"
WEIGHT="$3"

echo "+++"
echo "title = \"$TITLE\""
echo "template = \"$TEMPLATE\""
if [ -n "$WEIGHT" ]; then
    echo "weight = $WEIGHT"
fi
echo "+++"
# Add a newline after the frontmatter closing for better markdown rendering
cat -
 
