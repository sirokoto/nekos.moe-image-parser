import requests as rq
import argparse as ap
from re import search
from pathlib import Path
from datetime import datetime 
from json import dumps
from time import sleep


def check_if_directory_exists_and_make_dir(date_directory: Path) -> Path:
    target_directory = date_directory.joinpath(f"{datetime.now().date()}")
    if not target_directory.exists():
        target_directory.mkdir()
    return target_directory
def get_max_image_index(directory: Path):
    date_directories = [x for x in directory.iterdir() if x.is_dir()]
    directories_dictionary: dict[Path,list[Path]]= {}
    max_file_index_per_directory = {}
    for _dir in date_directories:
        for directories_path,_,files in _dir.walk(on_error=print):
            directories_dictionary[directories_path] = [directories_path/file for file in files]
        max_file_index_per_directory = {
            folder: max((int(m.group(1)) for f in files if (m := search(r"^image_(\d+)\.[^.]+$", f.name))),
                        default=0) for folder, files in directories_dictionary.items()}
    return max_file_index_per_directory
def get_neko_image(directory: Path, headers):
    data = rq.get("https://nekos.moe/api/v1/random/image?nsfw=false", headers=headers)
    json_inf = data.json()
    id = json_inf["images"][0]["id"]
    image_url = f"https://nekos.moe/image/{id}"
    image = rq.get(image_url)
    target_file_directory = check_if_directory_exists_and_make_dir(directory)
    image_filename = target_file_directory/f"image_{get_max_image_index(directory)[target_file_directory]+1:03d}.png"
    with open(image_filename, "wb") as f:f.write(image.content)
    return image_filename
def run_neko(args, headers):
    iterations: int = int(args.iterations)
    if iterations > 1:
        for i in range(iterations):
            if i%5 == 0 and i != 0:
                sleep(5)
            print(f"writed {get_neko_image(args.directory, headers=headers)} file")
    else:
        print(f"writed {get_neko_image(args.directory, headers=headers)} file")
def list_tags_on_waifu_im():
    data = rq.get("https://api.waifu.im/tags")
    json_inf = data.json()
    tags = dumps(json_inf, indent=4)
    print(tags)
def run_waifu():
    url = "https://api.waifu.im/images"
    if input("Do you want NSFW enabled (y/N)? ").lower() == "y":
        params = {
            'IsNsfw': 'true',
            'IncludedTags': ['uniform',]
        }
        data = rq.get(url, params=params)
        json_inf = data.json()
        image = rq.get(json_inf["images"][0]["url"])
        with open("waifu_nsfw.png", "wb") as f: 
            f.write(image.content)
    else:
        params = {
            'IncludedTags': ['maid',],
            'Height': '>=1080'
        }
        data = rq.get(url, params=params)
        json_inf = data.json()
        image = rq.get(json_inf["items"][0]["url"])
        with open("waifu.png", "wb") as f: 
            f.write(image.content)
def main():
    parser = ap.ArgumentParser(description="A tool for getting neko and waifu images")
    parser.add_argument("-d", "--directory", help="Where downloaded images to be put", type=Path, default=Path('./target'))
    parser.add_argument("-l", '--iterations', default=1, help="Iterations", type=int)
    parser.add_argument('-t', '--test', help="Iterations", action="store_true")
    parser.add_argument("choice", help="Choose between Neko and Waifu", choices=["Neko","Waifu","neko","waifu"], default="neko")
    args = parser.parse_args()
    headers = {
        "User-Agent": "Nekos.moe parser (https://github.com/sirokoto/nekos.moe-image-parser 1.0.0)"
    }
    if args.test:
        run_neko(args, headers=headers)
    else:
        match(args.choice.lower()):
            case "neko": run_neko(args, headers=headers)
            case "waifu": run_waifu()
            case "tags": list_tags_on_waifu_im()
if __name__ == "__main__":
    main()
