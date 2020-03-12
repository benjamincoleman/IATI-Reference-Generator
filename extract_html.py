import os
import shutil
from bs4 import BeautifulSoup


if os.path.exists("output.zip"):
    os.remove("output.zip")
if os.path.isdir("output"):
    shutil.rmtree("output")


build_dirs = {
    "203": "IATI-Standard-SSOT-version-2.03/docs/en/_build/dirhtml",
    "202": "IATI-Standard-SSOT-version-2.02/docs/en/_build/dirhtml",
    "201": "IATI-Standard-SSOT-version-2.01/docs/en/_build/dirhtml",
    "105": "IATI-Standard-SSOT-version-1.05/docs/en/_build/dirhtml",
    "104": "IATI-Standard-SSOT-version-1.04/docs/en/_build/dirhtml",
    "guidance": "IATI-Guidance/en/_build/dirhtml",
    "developer-documentation": "IATI-Developer-Documentation/_build/dirhtml"
}

ignore_dirs = [
    "404",
    "CONTRIBUTING",
    "genindex",
    "gsearch",
    "license",
    "README",
    "search",
    "sitemap"
]


for parent_slug, root_dir in build_dirs.items():
    for dirname, dirs, files in os.walk(root_dir, followlinks=True):
        dir_split = dirname.split(os.path.sep)
        root_len = len(root_dir.split(os.path.sep))
        if len(dir_split) == root_len or dir_split[root_len] not in ignore_dirs:
            if "index.html" in files:
                input_path = os.path.join(dirname, "index.html")
                with open(input_path, 'r') as input_html:
                    soup = BeautifulSoup(input_html.read(), 'html.parser')
                    main = soup.find("div", {"role": "main"})
                    pre_spans = main.findAll("span", attrs={'class': 'pre'})
                    for pre_span in pre_spans:
                        pre_span.name = 'pre'
                    for tag in main():
                        for attribute in ["class", "style"]:
                            del tag[attribute]
                    output_dir = os.path.join("output", parent_slug, *dir_split[root_len:])
                    output_path = os.path.join(output_dir, "index.html")
                    if not os.path.isdir(output_dir):
                        os.makedirs(output_dir)
                    with open(output_path, 'w') as output_xml:
                        output_xml.write(str(main))