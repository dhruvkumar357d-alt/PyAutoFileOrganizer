# File Organizer

My Downloads folder was a mess, so I wrote a small Python script that sorts files into folders by type. It uses only the standard library, so there's nothing to install.

Before:

```
Downloads/
├── resume.pdf
├── holiday.jpg
├── song.mp3
├── project.zip
└── notes.txt
```

After:

```
Downloads/
├── Documents/   (resume.pdf, notes.txt)
├── Images/      (holiday.jpg)
├── Audio/       (song.mp3)
└── Archives/    (project.zip)
```

## Usage

You need Python 3.6 or newer.

```bash
python organizer.py --path ~/Downloads --dry-run   # preview only
python organizer.py --path ~/Downloads             # actually move files
```

If you leave out `--path`, it organizes the folder you're currently in. Be careful with that one.

| Flag | What it does |
|------|--------------|
| `--path` | Folder to organize (default: current folder) |
| `--dry-run` | Prints what would move, changes nothing |

## How it works

- Files are sorted by extension: Documents, Images, Audio, Video, Archives and Code. Anything else goes to `Others`.
- If a file with the same name already exists in the target folder, the new one is renamed (`report.pdf` becomes `report_1.pdf`). Nothing gets overwritten.
- Hidden files (like `.DS_Store`), existing subfolders and the script itself are left alone.
- If one file can't be moved (permissions, file in use), the error is logged and the script carries on with the rest.

## Safety notes

The script never deletes or overwrites files, but it does move them, and there's no undo. To stay safe:

- Run with `--dry-run` first and read the list.
- Always pass an explicit `--path` (for example `~/Downloads`).
- Don't run it on project folders or program folders, since moving files can break things that expect them in a certain place.
- If you run it by accident, your files are still inside the folder you pointed it at. You'd just have to sort them back by hand.

## Changing the categories

The categories live in the `FILE_CATEGORIES` dictionary at the top of `organizer.py`. To add a type, add its extension to a list. To add a category, add a new key:

```python
"Ebooks": ['.epub', '.mobi'],
```

## Tests

```bash
pip install pytest
pytest
```

## Limitations

- Only looks at the top level of the folder and doesn't go into subfolders.
- Sorts by extension only, so a renamed file will end up in the wrong place.
- No undo (see safety notes above).

## Contributing

Bug reports and pull requests are welcome. If you're adding a feature, please open an issue first so we can talk it through.

## License

MIT. See [LICENSE](LICENSE).
