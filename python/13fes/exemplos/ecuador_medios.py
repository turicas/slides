#!/usr/bin/env python
# coding: utf-8

# Create by Álvaro Justen <https://github.com/turicas>
# requirements:
# pip install requests
# pip install git+https://github.com/turicas/rows.git

from collections import OrderedDict
from io import BytesIO
from urlparse import urljoin

import requests
import rows


URLS = ['http://www.supercom.gob.ec/es/informate-y-participa/directorio-de-medios/21-radiodifusoras',
        'http://www.supercom.gob.ec/es/informate-y-participa/directorio-de-medios/22-television',
        'http://www.supercom.gob.ec/es/informate-y-participa/directorio-de-medios/23-prensa']
rows_xpath = '//*[@class="entry-container"]/*[@class="row-fluid"]/*[@class="span6"]'
fields_xpath = OrderedDict([
        ('url', '//h2/a/@href'),
        ('name', '//h2/a/text()'),
        ('address', '//div[@class="spField field_direccion"]/text()'),
        ('phone', '//div[@class="spField field_telefono"]/text()'),
        ('website', '//div[@class="spField field_sitio_web"]/text()'),
        ('email', '//div[@class="spField field_email"]/text()'), ])
field_types = fields_xpath.copy()
for field_name in field_types.keys():
    # We're going to force the field types (instead of using automatic
    # detection) since some pages will identify "email" field as `EmailField`
    # and other as `TextField` (because the data is wrong: they've put website
    # into "email" field on some rows).
    field_types[field_name] = rows.fields.TextField
final_fields = field_types.copy()
final_fields['category'] = rows.fields.TextField


def import_data(url):
    'Make HTTP request and import data using XPath'

    response = requests.get(url)
    return rows.import_from_xpath(BytesIO(response.content),
                                  rows_xpath,
                                  fields_xpath,
                                  fields=field_types)


def download_all_pages(url):
    'Given a URL, download all the pages using `site=PAGENUMBER` querystring'

    category = url.split('-')[-1]
    print 'Downloading {}...'.format(category)

    tables = []
    finished = False
    page = 1
    while not finished:
        print '  - Page {}...'.format(page),
        table = import_data(url + '?site={}'.format(page))
        if len(table):
            tables.append(table)
            page += 1
            print 'ok'
        else:
            finished = True
            print 'empty (finished)'

    return sum(tables)


def transform(row, table, url):
    "Fix row's URL (to be absolute) and add `category` field"

    data = row._asdict()

    data['url'] = urljoin(url, data['url'])  # put absolute URL
    data['category'] = url.split('-')[-1]

    return data


def main():
    tables = [rows.transform(final_fields,
                             lambda row, table: transform(row, table, url),
                             download_all_pages(url))
              for url in URLS]
    rows.export_to_csv(sum(tables), 'ecuador-medios.csv')


if __name__ == '__main__':
    main()