import requests as rq
import argparse as ap
from re import search
import os, sys, datetime
from json import dumps
from time import sleep

def check_if_directory_exists_and_make_dir(dirc):
    Dir = f"{dirc.__str__()}/{datetime.datetime.now().date()}"
    if not os.path.exists(Dir):
        os.mkdir(Dir)
    return Dir
def get_max_image_index(Dir: str):
    targetDirs = lambda x: [f"{Dir}/%s" % i for i in x]
    targetFiles = lambda x,y: f"{x}/%s" % y
    dirList = os.listdir(Dir) # date dirs
    dirs_full = targetDirs(dirList)
    files: list[str] = []
    dirs_dict = {}
    max_per_dir = {}
    #print(dirs_full)
    for _dir in dirs_full:
        files_in_dir = os.listdir(_dir)
        for dirpath,_,f in os.walk(_dir):
            dirs_dict[dirpath] = [f"{dirpath}/{file}" for file in f]
        max_per_dir = {folder: max((int(m.group(1)) for f in files if (m:= search(r"^image_(\d+)\.[^.]+$", os.path.basename(f)))), default=0) for folder, files in dirs_dict.items()}
    return max_per_dir
def getNekoImage():
    data = rq.get("https://nekos.moe/api/v1/random/image?nsfw=false")
    json_inf = data.json()
    id = json_inf["images"][0]["id"]
    image_url = f"https://nekos.moe/image/{id}"
    image = rq.get(image_url)
    Dir = check_if_directory_exists_and_make_dir(args.directory)
    _dict = get_max_image_index(args.directory)    
    image_filename = f"{Dir}/image_{_dict[Dir]+1:03d}.png"
    with open(image_filename, "wb") as f:f.write(image.content)
def runNeko():
    iters: int = int(args.iterations)
    if args.iterations > 1:
        for i in range (args.iterations):
            if i%5 == 0 and i != 0:
                sleep(5)
            getNekoImage()
    else:
        getNekoImage(1)
def listTagsOnWaifuIm():
    data = rq.get("https://api.waifu.im/tags")
    json_inf = data.json()
    tags = dumps(json_inf, indent=4)
    print(tags)
def runWaifu():
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
        case "neko": runNeko()
        case "waifu": runWaifu()
        case "tags": listTagsOnWaifuIm()
if __name__ == "__main__":
    main()
