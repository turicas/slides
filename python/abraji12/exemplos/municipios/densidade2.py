import rows

municipios = rows.import_from_csv('municipios-brasil.csv')
for municipio in municipios:
    if municipio.estado == 'RJ':
        densidade = municipio.habitantes / municipio.area
        print(municipio.nome + '/RJ' + ': ' + str(densidade) + ' hab/km²')
