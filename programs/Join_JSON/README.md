## 

### Join JSON Parts

Merge two JSON parts of the same PDF into one file:
- Keeps all metadata from part 1.
- Uses part 1 `text` as-is (retains its leading `markdown` marker).
- Appends part 2 `text` after stripping any leading `markdown` marker.
- Removes embedded `debug_data_path` markers inside the text and drops a root-level `debug_data_path` if present.


### How to Run
From the repo root:
```bash
python join_json.py
```
Custom names:
```bash
python join_json.py --part1 your_Part1.json --part2 your_Part2.json -o your_Combined.json
```

### Output
- Combined JSON with metadata from part 1 and Markdown text (part 1 then part 2, separated by a blank line), without debug markers.
