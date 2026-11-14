# Nekos.moe Image Downloader

A Python command-line tool for downloading random images from [nekos.moe](https://nekos.moe/).

Images are requested with `nsfw=false`, organized into dated folders, and saved with sequential filenames.

## Features

- Download multiple images in one run.
- Choose a custom download directory.
- Automatically create a folder for the current date.
- Continue numbering from the highest existing image index in that folder.
- Pause for five seconds between batches of five downloads.

## Requirements

- Python 3.10 or newer
- [requests](https://pypi.org/project/requests/)
- An internet connection

## Setup

From the directory containing `main.py`, install the dependency:

```bash
python -m pip install requests
```

Create the base download directory:

```bash
mkdir -p ./target
```

The base directory must already exist. The script creates the dated subdirectory inside it.

## Usage

```bash
python main.py neko [options]
```

### Download five images

```bash
python main.py neko -l 5
```

### Use a custom directory

Create the directory first, then start downloading:

```bash
mkdir -p ./images
python main.py neko -d ./images -l 10
```

### Download one image

After applying the single-download fix described under **Known issues**:

```bash
python main.py neko
```

### Show help

```bash
python main.py --help
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `choice` | Required positional argument. Use `neko` or `Neko`. | — |
| `-d`, `--directory` | Base directory for downloaded images. | `./target` |
| `-l`, `--iterations` | Number of images to download. Use a positive integer. | `1` |
| `-t`, `--test` | Accepted by the parser but currently has no effect. | Disabled |
| `-h`, `--help` | Display command-line help. | — |

## Output Structure

Downloads are grouped by the machine’s current local date:

```text
target/
└── YYYY-MM-DD/
    ├── image_001.png
    ├── image_002.png
    └── image_003.png
```

Running the tool again on the same day continues numbering after the highest existing image index.

## Known Issues

- **Single-image downloads:** `runNeko()` currently calls `getNekoImage(1)`, but `getNekoImage()` takes no arguments. Replace that call with `getNekoImage()` before using the default iteration count.
- **Directory scanning:** Keep the base download directory dedicated to date folders. The current scanner assumes its immediate children are directories.
- **Image format:** Every download receives a `.png` extension, but the script does not convert the image data to PNG.
- **Network errors:** Requests currently have no explicit timeouts or HTTP status checks.
