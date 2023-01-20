import re
import urllib.parse
from bs4 import BeautifulSoup


def learner_generator(soup):
    keyword_seperator = re.compile(r"[/◆\(]")
    crosslink_re = re.compile(r'href="#(calibre_link[^"]*)"')
    keywords = []
    ids = {}

    def crosslink_repl(match):
        id = match.group(1)
        return 'href="entry://{}#{}"'.format(ids[id], id)

    for heading in soup.findAll('p', class_="calibre_1"):
        # fetch keyword from heading
        keyword = ' '.join(keyword_seperator.split(heading.get_text())[
            0].split()).strip().replace('|', '')

        nodes = [heading]
        current_node = heading
        while current_node.nextSibling is not None:
            current_node = current_node.nextSibling
            if (current_node.name == 'p' and current_node.attrs['class'] == ['calibre_1']) or (current_node.name == 'div' and current_node.attrs['class'] == ['mbp_pagebreak']):
                break
            nodes.append(current_node)

        keywords.append((keyword, nodes))
        for node in nodes:
            if node.name is not None:
                if 'id' in node.attrs:
                    ids[node.attrs['id']] = urllib.parse.quote(
                        keyword, safe='')
                for anchor in node.findAll(id=True):
                    ids[anchor.attrs['id']] = urllib.parse.quote(
                        keyword, safe='')

    for (keyword, nodes) in keywords:
        yield (keyword, crosslink_re.sub(crosslink_repl, "\r\n".join(map(str, nodes))).strip())


with open("index.html") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

with open("output.txt", "wb") as f:
    for (k, d) in learner_generator(soup):
        f.write(k.encode("utf-8"))
        f.write(b'\r\n<link rel="stylesheet" type="text/css" href="style.css" />\r\n')
        f.write(d.encode("utf-8"))
        f.write(b'\r\n</>\r\n')
