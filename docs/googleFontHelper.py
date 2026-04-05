import requests

debug = False


# request against a URL
def download_file(url, target_dir="stylesheets/fonts/"):
    local_filename = url.split("/")[-1]
    # NOTE the stream=True parameter below
    with requests.get(url) as r:
        r.raise_for_status()
        with open(target_dir + local_filename, "wb") as f:
            f.write(r.content)
    return local_filename


all_links_for_download = ""
# this original file can be obtained from the website source
# from a standard zensical docs page, it is included for reference if
# you want to reproduce this script
with open("stylesheets/_generated_fromZensicalGoogle_extra.css", "r") as cssFonts:
    lines = cssFonts.readlines()
    for line in lines:
        # now we get all relevant urls to serve the fonts from our own server
        if "url(https" in line:
            download_file(
                "https" + line.split("https")[1].split(".woff2")[0] + ".woff2"
            )
            if debug:
                all_links_for_download += (
                    "https" + line.split("https")[1].split(".woff2")[0] + ".woff2\n"
                )

# user now only needs to search + replace the URLs in the extra css with local
# paths obtained from this script

if debug:
    print(f"{all_links_for_download=}")
    # store the obtained font woffs for reference
    with open("fonts_woffs.txt", "w") as fontsLinks:
        fontsLinks.write(all_links_for_download)
