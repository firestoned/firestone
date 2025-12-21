import sys
import re


def fix_anchors():
    content = sys.stdin.read()

    # Pattern to find <a id="..."></a> followed eventually by a header
    # We need to capture the ID and the Header content

    # Strategy: Iterate line by line.
    # If we see <a id="...">, store the ID.
    # If we see a header #..., and we have a stored ID, append the ID to the header and clear stored ID.
    # If we see other text, print it.

    lines = content.splitlines()
    pending_id = None

    anchor_pattern = re.compile(r'<a id="([^"]+)"></a>')
    header_pattern = re.compile(r"^(#+)\s+(.*)")

    for line in lines:
        anchor_match = anchor_pattern.search(line)
        if anchor_match:
            pending_id = anchor_match.group(1)
            # Don't print the anchor line
            continue

        header_match = header_pattern.match(line)
        if header_match and pending_id:
            level = header_match.group(1)
            text = header_match.group(2)
            # Zola syntax for custom ID: # Title {#id}
            print(f"{level} {text} {{#{pending_id}}}")
            pending_id = None
        else:
            print(line)


if __name__ == "__main__":
    fix_anchors()
