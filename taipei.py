# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs


url_pattern = "https://cloud.taipei/{}"
def get_welfare_base_urls():
    base_url = "https://cloud.taipei/web_swc_getCategory"
    r = requests.get(base_url)
    soup = bs(r.content, 'html.parser')
    anchors = soup.select("a")
    links = [url_pattern.format(a["href"]) for a in anchors if a["href"].startswith("web_swc_getList2")]
    return links


def get_welfare_info_urls(links):
    info_urls = []
    for link in links:
        r = requests.get(link)
        _soup = bs(r.content, 'html.parser')
        name_tags = _soup.find_all('td', {"data-title": "名稱"})
        for _tag in name_tags:
            info_urls.append(_tag.a["href"])
            print(info_urls)
    return info_urls


def get_welfare_infos(urls):
    welfare_infos = []
    for url in urls:
        url = url_pattern.format(url)
        r = requests.get(url)
        _soup = bs(r.content, 'html.parser')
        table_head = _soup.select(".article")[0]
        table_content = _soup.select(".article")[1]
        org_infos = table_content.select("tr")
        info = {
            "org_name": table_head.select("h1.left")[0].text,
            "pub_admin": table_head.select("div.left")[0].text,
            "org_type": org_infos[0].select("td")[1].text,
            "org_name": org_infos[2].select("td")[1].text,
            "org_phone": org_infos[4].select("td")[1].text,
            "org_address": org_infos[5].select("td")[1].text,
            "org_client": org_infos[6].select("td")[1].text,
        }
        welfare_infos.append(info)
    print(welfare_infos)
    return welfare_infos


if __name__ == "__main__":
    links = get_welfare_base_urls()
    info_urls = get_welfare_info_urls(links)
    welfare_infos = get_welfare_infos(info_urls)
