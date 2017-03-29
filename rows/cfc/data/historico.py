import rows
municipios = rows.import_from_csv('brazilian-cities.csv')
municipios[0]
for municipio in municipios:
    print(municipio)
[municipio.inhabitants for municipio in municipios if municipio.state == 'SC']
sum([municipio.inhabitants for municipio in municipios if municipio.state == 'SC'])
total = 0
for municipio in municipios:
    if municipio.state == 'SC':
        total += municipio.inhabitants
total
sum(municipio.inhabitants for municipio in municipios if municipio.state == 'SC')
densidades = [(municipio.city, municipio.inhabitants / municipio.area) for municipio in municipios if municipio.state == 'SC']
densidades
densidades = [(municipio.city, municipio.inhabitants / municipio.area) for municipio in municipios if municipio.state == 'SC']
densidades.sort(key=lambda row: row[1], reverse=True)
densidades
for item in densidades:
    print('{} -> {:5.2f}'.format(item[0], item[1]))
for item in densidades:
    print('{} -> {:5.2f}hab/km²'.format(item[0], item[1]))
%hist
municipios
municipios.fields
municipios['densidade'] = [row.inhabitants / row.area for row in municipios]
municipios
municipios.fields
municipios.order_by('-densidade')
municipios[0]
municipios[-1]
municipios['densidade'] = [row.inhabitants / row.area for row in municipios]
municipios['densidade']
sum(municipios['inhabitants'])
municipios['densidade'] = [row.inhabitants / row.area for row in municipios]
data = [{'city': municipio.city, 'density': municipio.inhabitants / municipio.area} for municipio in municipios if municipio.state == 'SC']
data[0]
dsc = rows.import_from_dicts(data)
dsc
rows.export_to_html(dsc, 'densidade-sc.html')
!google-chrome densidade-sc.html
html = rows.export_to_html(dsc)
print(html.read())
print(html)
%hist
print(rows.export_to_txt(dsc))
dsc
print(rows.export_to_txt(municipios))
del municipios['inhabitants']
del municipios['arae']
del municipios['area']
print(rows.export_to_txt(municipios))
import glob
glob.glob('*.csv')
glob.glob('*.*')
municipios
sc = rows.import_from_dicts([{'city': row.city, 'density': row.densidade} for row in municipios if row.state == 'SC'])
rs = rows.import_from_dicts([{'city': row.city, 'density': row.densidade} for row in municipios if row.state == 'RS'])
pr = rows.import_from_dicts([{'city': row.city, 'density': row.densidade} for row in municipios if row.state == 'PR'])
sc.fields
rs.fields
pr.fields
sc
rs
pr
sul = sc + pr + rs
sul


import rows
table = rows.import_from_html('mulheres.html', preserve_html=True)
for row in table:
    print(row.mulheres)
tag = '<a href="http://youtube.com/c/PythonicCafe">Canal no YouTube</a>'
rows.plugins.html.tag_to_dict(tag)
rows.plugins.html.extract_links?



---

vim tania.py
ipython -i tania.py
vim tania.py
ipython -i tania.py
rows print 'http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=130&codv=v01&search=santa-catarina|florianopolis|sintese-das-informacoes-'
rows print --input-locale='pt_BR.UTF-8' 'http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=130&codv=v01&search=santa-catarina|florianopolis|sintese-das-informacoes-'
rows convert --input-locale='pt_BR.UTF-8' 'http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=130&codv=v01&search=santa-catarina|florianopolis|sintese-das-informacoes-' populacao-sc.json
python3 -m http.server
rows query --input-locale='pt_BR.UTF-8' 'SELECT municipio, pessoas FROM table1 ORDER BY pessoas DESC' 'http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=130&codv=v01&search=santa-catarina|florianopolis|sintese-das-informacoes-'
time rows query --input-locale='pt_BR.UTF-8' 'SELECT municipio, pessoas FROM table1 ORDER BY pessoas DESC' 'http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=130&codv=v01&search=santa-catarina|florianopolis|sintese-das-informacoes-'
POPULACAO_SC='http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=130&codv=v01&search=santa-catarina|florianopolis|sintese-das-informacoes-'
HOMENS='http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=1&codv=v04&search=santa-catarina|florianopolis|sintese-das-informacoes-'
MULHERES='http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=1&codv=v07&search=santa-catarina|florianopolis|sintese-das-informacoes-'
rows print $HOMENS
rows print --input-locale=pt_BR.UTF-8 $HOMENS
rows print --input-locale=pt_BR.UTF-8 $MULHERES
rows query --input-locale=pt_BR.UTF-8 'SELECT table1.municipio AS municipio, (100.0 * table2.mulheres) / (table1.homens + table2.mulheres) AS perc_mulheres WHERE table1.municipio = table2.municipio' $HOMENS $MULHERES
rows query --input-locale=pt_BR.UTF-8 'SELECT table1.municipio AS municipio, (100.0 * table2.mulheres) / (table1.homens + table2.mulheres) AS perc_mulheres FROM table1, table2 WHERE table1.municipio = table2.municipio' $HOMENS $MULHERES
rows query --input-locale=pt_BR.UTF-8 'SELECT table1.municipio AS municipio, (100.0 * table2.mulheres) / (table1.homens + table2.mulheres) AS perc_mulheres FROM table1, table2 WHERE table1.municipio = table2.municipio ORDER BY perc_mulheres DESC' $HOMENS $MULHERES
rows query --input-locale=pt_BR.UTF-8 'SELECT table1.municipio AS municipio, (100.0 * table2.mulheres) / (table1.homens + table2.mulheres) AS perc_mulheres FROM table1, table2 WHERE table1.municipio = table2.municipio ORDER BY perc_mulheres DESC' $HOMENS $MULHERES --output=mulheres-sc.csv
ipython
wget -O mulheres.html 'http://www.cidades.ibge.gov.br/comparamun/compara.php?lang=&coduf=42&idtema=1&codv=v07&search=santa-catarina|florianopolis|sintese-das-informacoes-'
vim mulheres
vim mulheres.html
ipython
history


workon rows3
cd projects/slides/rows/fisl17/data/
ipython
rows
ls -lh
rows print bc.xls
#rows print bc.xls
rows
rows query 'SELECT state, city, inhabitants FROM table1 ORDER BY inhabitants DESC' bc.xls
rows query 'SELECT state, city, inhabitants FROM table1 ORDER BY inhabitants DESC' bc.xls --output=resultado.csv
vim resultado.csv
#http://bit.ly/rows-pybr12
rows query 'SELECT city, (inhabitants / area) AS density FROM table1 WHERE state = "SC" ORDER BY density DESC' bc.xls
rows query 'SELECT city, (inhabitants / area) AS density FROM table1 WHERE state = "SC" ORDER BY density DESC' bc.xls --output=densidade-sc.csv
vim densidade-sc.csv
ipython
rows query
rows query --help
rows query 'SELECT city, (inhabitants / area) AS density FROM table1 WHERE state = "SC" ORDER BY density DESC' bc.xls --output=densidade-sc.json
google-chrome densidade-sc.json
python3 http.server
python3 -m http.server
vim sc.txt
rows query 'select * from table1 where density < 100' sc.txt

