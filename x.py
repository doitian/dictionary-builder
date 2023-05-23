#!/usr/bin/env python3
import re
import urllib.parse
from bs4 import BeautifulSoup

# ruff: noqa: E501


def get_text(node):
    return str(node).replace("\n", "\r\n").replace('src="images/', 'src="/images/')


def learner_generator(soup):
    keyword_seperator = re.compile(r"[/◆\(]")  # )
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


def merriam_websters_collegiate_dictionar_11_generator(soup):
    crosslink_re = re.compile(r'href="#(calibre_link[^"]*)"')
    keywords = []
    ids = {}

    def crosslink_repl(match):
        id = match.group(1)
        if id in ['calibre_link-87148', 'calibre_link-87149', 'calibre_link-87150', 'calibre_link-87151', 'calibre_link-87152', 'calibre_link-87153', 'calibre_link-87154', 'calibre_link-87155', 'calibre_link-87156', 'calibre_link-87157', 'calibre_link-87158', 'calibre_link-87159']:
            return match.group(0)
        return 'href="entry://{}#{}"'.format(ids[id], id)

    for heading in soup.findAll('dfn', title=True):
        keyword = heading.attrs['title']
        node = heading.parent

        if len(keywords) > 0 and keywords[-1][0] == keyword:
            keywords[-1][1].append(node)
        else:
            keywords.append((keyword, [node]))

        if 'id' in node.attrs:
            ids[node.attrs['id']] = urllib.parse.quote(
                keyword, safe='')
        for anchor in node.findAll(id=True):
            ids[anchor.attrs['id']] = urllib.parse.quote(
                keyword, safe='')

    for table in soup.findAll('table', id=True):
        keyword = table.find('th').get_text().strip()
        ids[table.attrs['id']] = urllib.parse.quote(keyword, safe='')
        keywords.append((keyword, [table]))

    ids["calibre_link-76236"] = urllib.parse.quote("alphabet table", safe="")
    keywords.append(("Alphabet Table", [
                    '<div id= class="calibre_4"><img alt="alphabet table" src="images/000592.jpg" class="calibre2" /></div>']))

    for (id, keyword) in [("calibre_link-76629", "Numbers Table")]:
        ids[id] = urllib.parse.quote(keyword, safe='')
        nodes = [soup.find(id=id)]
        current_node = nodes[0]
        while current_node.nextSibling is not None:
            current_node = current_node.nextSibling
            if current_node.name is not None and 'mbp_pagebreak' in current_node.attrs['class']:
                break
            else:
                nodes.append(current_node)

    for (keyword, nodes) in keywords:
        yield (keyword, crosslink_re.sub(crosslink_repl, "\r\n".join(map(get_text, nodes))).strip())


def merriam_websters_collegiate_thesaurus_2_generator(soup):
    crosslink_re = re.compile(r'href="#(calibre_link[^"]*)"')
    keywords = []
    ids = {}

    def crosslink_repl(match):
        id = match.group(1)
        return 'href="entry://{}#{}"'.format(ids[id], id)

    for node in soup.findAll('div', class_='calibre_13'):
        heading = node.find('span', class_='bold')
        if heading is None:
            continue

        keyword = heading.get_text().strip()

        if len(keywords) > 0 and keywords[-1][0] == keyword:
            keywords[-1][1].append(node)
        else:
            keywords.append((keyword, [node]))

        if 'id' in node.attrs:
            ids[node.attrs['id']] = urllib.parse.quote(
                keyword, safe='')
        for anchor in node.findAll(id=True):
            ids[anchor.attrs['id']] = urllib.parse.quote(
                keyword, safe='')

    for (keyword, nodes) in keywords:
        yield (keyword, crosslink_re.sub(crosslink_repl, "\r\n".join(map(get_text, nodes))).strip())


def merriam_websters_synonyms_and_antonyms_generator(soup):
    crosslink_re = re.compile(r'href="#(calibre_link[^"]*)"')
    keywords = []
    ids = {}

    def crosslink_repl(match):
        id = match.group(1)
        return 'href="entry://{}#{}"'.format(ids[id], id)

    for node in soup.findAll('div', class_='calibre_13'):
        heading = node.select_one('.calibre10 .bold')
        if heading is None:
            continue

        keyword = heading.get_text().strip()

        if len(keywords) > 0 and keywords[-1][0] == keyword:
            keywords[-1][1].append(node)
        else:
            keywords.append((keyword, [node]))

        if 'id' in node.attrs:
            ids[node.attrs['id']] = urllib.parse.quote(
                keyword, safe='')
        for anchor in node.findAll(id=True):
            ids[anchor.attrs['id']] = urllib.parse.quote(
                keyword, safe='')

    for (keyword, nodes) in keywords:
        yield (keyword, crosslink_re.sub(crosslink_repl, "\r\n".join(map(get_text, nodes))).strip())


def merriam_websters_vocabulary_builder_generator(soup):
    crosslink_re = re.compile(r'href="#(calibre_link[^"]*)"')
    keywords = []
    root = None
    ids = {}

    def crosslink_repl(match):
        id = match.group(1)
        return 'href="entry://{}"'.format(ids[id])

    for node in soup.findAll('p', class_='calibre9'):
        heading = node.select_one('b.calibre3')
        if heading is None:
            continue
        keyword = heading.get_text().strip()

        idNode = node.previousSibling
        if idNode is not None and idNode.name == 'hr':
            idNode = idNode.previousSibling.previousSibling
            root = keyword
        elif keyword == 'halcyon':
            root = None
        if idNode is None or idNode.name != 'a':
            continue

        ids[idNode.attrs['id']] = urllib.parse.quote(keyword, safe='')

        keywords.append((keyword, root, [node]))

    for (keyword, root, nodes) in keywords:
        body = crosslink_re.sub(
            crosslink_repl, "\r\n".join(map(get_text, nodes))).strip()
        if root is not None and root != keyword:
            body = '<p><strong>Root: </strong> ' + \
                ', '.join(
                    f'<a href="entry://{r}">{r}</a>' for r in root.split('/')) + '</p>' + body
        for variant in keyword.split('/'):
            yield (variant, body)


with open("index.html") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

with open("output.txt", "wb") as f:
    for (k, d) in merriam_websters_vocabulary_builder_generator(soup):
        f.write(k.encode("utf-8"))
        f.write(b'\r\n<link rel="stylesheet" type="text/css" href="style.css" />\r\n')
        f.write(d.encode("utf-8"))
        f.write(b'\r\n</>\r\n')
