import requests
from .cryptojs_aes_port import decrypt
import subprocess
import os
import code
import sys
from tempfile import TemporaryFile

API_KEY = "0df14814b9e590a1f26d3071a4ed7974"
AES_KEY = b"267041df55ca2b36f2e322d05ee2c9cf"

def api_request(url):
    r = requests.get(
        f"https://twist.moe/api{url}",
        headers = {
            "x-access-token": API_KEY
        }
    )

    r.raise_for_status()
    return r.json()

def get_show_to_slug():
    shows_json = api_request("/anime")
    shows_jp = {
        i["title"]: i["slug"]["slug"] for i in shows_json
    }

    return shows_jp

def get_title_translations():
    shows_json = api_request("/anime")
    translation = {
        i["title"]: i["alt_title"] for i in shows_json
    }

    for title in translation:
        if translation[title] is None:
            translation[title] = title

    translation = {
        translation[x]: x for x in translation
    }

    return translation

def get_source(slug, ep_number, use_aircdn=False):
    sources = api_request(f"/anime/{slug}/sources")
    encrypted_url = list(filter(lambda ep: ep["number"] == ep_number, sources))[0]["source"]
    url = decrypt(AES_KEY, encrypted_url)
    
    cdn = "air-" if use_aircdn else ""
    src_url = f"https://{cdn}cdn.twist.moe" + url
    
    return src_url

def get_num_episodes(slug):
    sources = api_request(f"/anime/{slug}/sources")
    return len(sources)

def download(slug, ep, out=None):
    out = out if out else f"{slug}/{slug}-{ep}.mp4"
    url = get_source(slug, ep)
    
    if not os.path.exists(slug):
        os.mkdir(slug)
    
    p = subprocess.Popen(["wget", "-c", "--retry-connrefused", "--tries=0", "--timeout=2", "--wait=1", "--header=Referer: https://twist.moe/", "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36", "-v", url, "-O", out])
    retcode = p.wait()
    return retcode

def stream(slug, ep_number):
    url = get_source(slug, ep_number)
    p = subprocess.Popen(["mpv", "--http-header-fields=Referer: https://twist.moe/", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    retcode = p.wait()

    return retcode == 4

if __name__ == "__main__":
    print(get_source("kono-subarashii-sekai-ni-shukufuku-wo", 1))
    download("kono-subarashii-sekai-ni-shukufuku-wo", 1)
    # stream("kobayashi-san-chi-no-maid-dragon", 6)
