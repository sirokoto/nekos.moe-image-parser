import requests as rq
import argparse as ap

parser = ap.ArgumentParser(description="A tool for getting neko images")
parser.add_argument("var", help="Choose between Neko and Waifu", type=str, default="nekos")
args = parser.parse_args()
def runNeko():
    data = rq.get("https://nekos.moe/api/v1/random/image?nsfw=false")
    json_inf = data.json()
    id = json_inf["images"][0]["id"]
    image_url = f"https://nekos.moe/image/{id}"
    image = rq.get(image_url)
    open("kitty.png", "wb").write(image.content)

def runWaifu():
    base_url = "https://api.waifu.im/search?"
    extra_tags_answer = input("Do you want to enable additional tags? (y/N)")
    if extra_tags_answer.lower() == "y":
        tags = input("Enter tags through space\nFor example: maid height=>=2000\nTags: ")
        url = f"{base_url}included_tags={tags.replace(" ", "&")}"
    elif extra_tags_answer.lower() == "n":
        url = "https://api.waifu.im/search"
    else: url = "https://api.waifu.im/search"
    data = rq.get(url)
    json_inf = data.json()
    image = rq.get(json_inf["images"][0]["url"])
    open("waifu.png", "wb").write(image.content)
    
if __name__ == "__main__":
    if args.var.lower() == "neko":
        runNeko()
    elif args.var.lower() == "waifu":
        runWaifu()
