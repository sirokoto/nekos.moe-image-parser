import requests as rq
import argparse as ap
from re import search
import os, sys, datetime
from json import dumps
from time import sleep

def check_if_directory_exists_and_make_dir(dirc):
    target_directory = f"{dirc.__str__()}/{datetime.datetime.now().date()}"
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)
    return target_directory
def get_max_image_index(directory: str):
    target_directories = lambda x: [f"{directory}/%s" % i for i in x]
    targetFiles = lambda x,y: f"{x}/%s" % y
    date_directories = os.listdir(directory) # date dirs
    directories_path = target_directories(date_directories)
    files_path: list[str] = []
    directories_dictionary = {}
    max_file_index_per_directory = {}
    for _dir in directories_path:
        files_in_dir = os.listdir(_dir)
        for directories_path,_,files in os.walk(_dir):
            directories_dictionary[directories_path] = [f"{directories_path}/{file}" for file in files]
        max_file_index_per_directory = {folder: max((int(m.group(1)) for f in files_path if (m:= search(r"^image_(\d+)\.[^.]+$", os.path.basename(f)))), default=0) for folder, files in directories_dictionary.items()}
    return max_file_index_per_directory
def get_neko_image(args):
    data = rq.get("https://nekos.moe/api/v1/random/image?nsfw=false")
    json_inf = data.json()
    id = json_inf["images"][0]["id"]
    image_url = f"https://nekos.moe/image/{id}"
    image = rq.get(image_url)
    target_file_directory = check_if_directory_exists_and_make_dir(args.directory)
    _dict = get_max_image_index(args.directory)    
    image_filename = f"{target_file_directory}/image_{_dict[target_file_directory]+1:03d}.png"
    with open(image_filename, "wb") as f:f.write(image.content)
def run_neko(args):
    iterations: int = int(args.iterations)
    if args.iterations > 1:
        for i in range (args.iterations):
            if i%5 == 0 and i != 0:
                sleep(5)
            get_neko_image(args)
    else:
        get_neko_image(args)
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
        with open("waifu.png", "wb")as f: 
            f.write(image.content)
def main():
    parser = ap.ArgumentParser(description="A tool for getting neko and waifu images")
    parser.add_argument("choice", help="Choose between Neko and Waifu", choices=["Neko","Waifu","neko","waifu"], default="neko")
    parser.add_argument("-d", "--directory", help="Where downloaded images to be put", type=str, default='./target')
    parser.add_argument("-l", '--iterations', default=1, help="Iterations", type=int)
    parser.add_argument('-t', '--test', help="Iterations", action="store_true")
    args = parser.parse_args()    
    match(args.choice.lower()):
        case "neko": run_neko(args)
        case "waifu": run_waifu()
        case "tags": list_tags_on_waifu_im()
if __name__ == "__main__":
    main()
