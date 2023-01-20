import re
import urllib.parse
from bs4 import BeautifulSoup


def learner_generator(soup):
    keyword_seperator = re.compile(r"[/◆]")
    crosslink_re = re.compile(r'href="(calibre_link[^"]*)"')
    ids = {}
    for heading in soup.findAll('p', class_="calibre_1"):
        if 'id' in heading.attrs:
            keyword = keyword_seperator.split(heading.get_text())[0].strip().replace('|', '')
            ids[heading.attrs['id']] = urllib.parse.quote(keyword, safe='')
    def crosslink_repl(match):
        return "entry://{}".format(ids[match.group(1)])

    for heading in soup.findAll('p', class_="calibre_1"):
        # fetch keyword from heading
        keyword = keyword_seperator.split(heading.get_text())[0].strip().replace('|', '')

        nodes = [heading]
        current_node = heading
        while current_node.nextSibling is not None:
            current_node = current_node.nextSibling
            if (current_node.name == 'p' and current_node.attrs['class'] == ['calibre_1']) or (current_node.name == 'div' and current_node.attrs['class'] == ['mbp_pagebreak']):
                break
            nodes.append(current_node)

        yield (keyword, crosslink_re.sub(crosslink_repl, "\n".join(map(str, nodes))))


with open("index.html") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

for (k, d) in learner_generator(soup):
    print(k)
    print('<link rel="stylesheet" type="text/css" href="style.css" />')
    print(d)
    print('</>')
