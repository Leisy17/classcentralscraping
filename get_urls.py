import requests
from bs4 import BeautifulSoup
import re
import sys
import os
from deep_translator import GoogleTranslator

translator = GoogleTranslator(
    source='auto', target='hi')

sys.stdout = open('C:\log.text', 'w')
sys.stdout.close()
sys.stdout = sys.__stdout__

links = {''}


def translate_content(bs: BeautifulSoup):
    find_text = bs.find_all(text=True)
    texts_list = []
    elements_list = []
    for word in find_text:
        if re.match('\S', word.text):
            texts_list.append(word.text)
            elements_list.append(word)
    translated = translator.translate_batch(texts_list)
    for i, element in enumerate(elements_list):
        if re.match('\S', element.text):
            new_element = element.replace(element.text, translated[i])
            element.replace_with(new_element)
    return str(bs)


def write_html(link):
    try:
        filename = link[29:]
        if re.search('/$', filename):
            filename = filename[:-1]
        if filename in links:
            return
        links.add(filename)
        filename = f'site/{filename}'
        request = requests.get(link, headers=hdr)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        document_translated = translate_content(
            BeautifulSoup(request.content, 'html.parser'))
        with open(f'{filename}.html', 'w', encoding="utf-8") as f:
            f.write(document_translated)
    except:
        print(filename)


def start_with_word(get_link: str):

    if re.search('^/', get_link):
        write_html(f'https://www.classcentral.com{get_link}')

    elif re.search('^https://www.classcentral.com/', get_link):
        write_html(get_link)


site = "https://www.classcentral.com/"
hdr = {'User-Agent': 'Firefox/110.0'}
request = requests.get(site, headers=hdr)
bs = BeautifulSoup(request.content, "html.parser")
os.makedirs('site/', exist_ok=True)
try:
    document_translated = translate_content(bs)
    with open('site/index.html', 'w', encoding="utf-8") as f:
        f.write(document_translated)
except:
    pass


for link in bs.find_all("a"):
    get_link = link.get("href")
    start_with_word(get_link)
