import os
from splinter import Browser

os.makedirs('news-ifc', exist_ok=True)
browser = Browser('firefox')
browser.visit('http://eventos.ifc.edu.br/sepe/')

news = browser.find_by_xpath('.//div[@class="titulos"]/h2/a')
links = [(link.value, link['href']) for link in news]
print('Found {} links.'.format(len(links)))
for title, url in links:
    print('  Visiting', title)
    browser.visit(url)
    filename = 'news-ifc/{}.html'.format(title)
    with open(filename, mode='w', encoding='utf-8') as fobj:
        fobj.write(browser.html)
browser.quit()
