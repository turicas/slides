from splinter import Browser

# Abre navegador na página desejada
browser = Browser('firefox')
browser.visit('http://www.google.com/')

# Escreve termo de busca e clica no botão "Buscar"
browser.fill('q', 'splinter - python acceptance testing for web applications')
button = browser.find_by_name('btnG')
button.click()

# Verifica se a página do Splinter está nos resultados
if browser.is_text_present('splinter.readthedocs.io'):
    print("Yes, the official website was found!")
else:
    print("No, it wasn't found... We need to improve our SEO techniques")

# Fecha navegador
browser.quit()
