from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import re, csv

FULL_MONTHS = {'janeiro': 1,  'fevereiro': 2, u'março': 3,    'abril': 4,
               'maio': 5,     'junho': 6,     'julho': 7,     'agosto': 8,
               'setembro': 9, 'outubro': 10,  'novembro': 11, 'dezembro': 12}

MONTHS = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4,  'mai': 5,  'jun': 6,
          'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}

def get_content_select(URL):
    browser = get_browser(URL)
    el = browser.find_element_by_id('I')
    content_list = []
    for option in el.find_elements_by_tag_name('option'):
        content_list.append(option.text.strip())

    browser.quit()
    return content_list

def get_html_body(browser):
    data = browser.find_element_by_tag_name('body')
    html = data.get_attribute("innerHTML")
    return BeautifulSoup(html, "html.parser")

def get_browser(url):
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    browser = webdriver.Firefox(options=opts)
    browser.get(url)
    sleep(2)
    return browser

def set_filter(browser, select_id, label):
    el = browser.find_element_by_id(select_id)
    for option in el.find_elements_by_tag_name('option'):
        if str(option.text).strip() == label:
            option.click()
            break

    return browser

def set_filter_SINAN(browser, select_id, label):
    el = browser.find_element_by_id(select_id)
    for option in el.find_elements_by_tag_name('option'):
        if label in str(option.text).strip():
            option.click()
            break

    return browser

def set_col_filter_SINAN(browser, select_id):
    el = browser.find_element_by_id(select_id)
    el_list = []
    for option in el.find_elements_by_tag_name('option'):
        el_list.append(str(option.text).strip())

    check = False
    if 'Mês dos 1º(s) Sintoma(s)' in el_list:
        for option in el.find_elements_by_tag_name('option'):
            if 'Mês dos 1º(s) Sintoma(s)' == str(option.text).strip():
                option.click()
                check = True
                break
                return browser

    if check == False:
        if 'Mês do acidente' in el_list:
            for option in el.find_elements_by_tag_name('option'):
                if 'Mês do acidente' == str(option.text).strip():
                    option.click()
                    break
        else:
            for option in el.find_elements_by_tag_name('option'):
                if 'Mês da notificação' == str(option.text).strip():
                    option.click()
                    break

    return browser

def set_content_filter(browser, select_id, label):
    el = browser.find_element_by_id(select_id)
    el_list = el.find_elements_by_tag_name('option')
    for option in el_list:
        if el_list[0] == option:
            option.click()
            sleep(1)
        if str(option.text).strip() == label:
            option.click()
            break

    return browser

def set_filter_SIH(browser, select_id, label):
    el = browser.find_element_by_id(select_id)
    for option in el.find_elements_by_tag_name('option'):
        if str(option.text).strip() == 'Todas as categorias':
            option.click()
        if str(option.text).strip() == label:
            option.click()
            break

    return browser

def set_year_filter(browser):
    el = browser.find_element_by_id('A')
    el_list = el.find_elements_by_tag_name('option')
    for option in el_list:
        if el_list[0] == option:
            pass
        else:
            option.click()

    return browser

def set_year_filter_SINAN(browser, year):
    el = browser.find_element_by_id('A')
    el_list = el.find_elements_by_tag_name('option')
    for option in el_list:
        if str(option.text).strip() == str(el_list[0].text).strip():
            option.click()
        if option.text == year:
            option.click()

    return browser

def get_size_year_SINAN(URL):
    browser = get_browser(URL)
    el = browser.find_element_by_id('A')
    el_list = []
    [el_list.append(i.text.strip()) for i in el.find_elements_by_tag_name('option')]
    browser.quit()

    return el_list

def set_cause_filter_SIM(browser, label):
    browser.find_element_by_xpath('//*[@id="fig9"]').click()
    sleep(1)
    set_filter(browser, 'S9', label)
    browser.find_element_by_xpath('/html/body/center/div/form/div[4]/div[2]/div[2]/input[1]').click()

    return browser

def set_cause_filter_SIH(browser, label):
    browser.find_element_by_xpath('//*[@id="fig10"]').click()
    sleep(2)
    set_filter_SIH(browser, 'S10', label)
    sleep(2)
    browser.find_element_by_xpath('/html/body/div/div/center/div/form/div[4]/div[2]/div[2]/input[1]').click()

    return browser

def key_formatter(key):
    if '..' in key:
        key = key.replace('..', '')
    
    return key

def value_formatter(value):
    if '\n' in value:
        value = value.replace('\n', '')
    if '-' == value:
        value = 0
    try:
        if value.isnumeric():
            value = int(value)
    except:
        pass

    return value

def ibge_code_city_formatter(string):
    m = re.search(r'[a-zA-Z]', string)
    index = m.start()
    ibge_code = string.split(string[index-1])[0]
    city_name = string.replace(ibge_code, '')
    
    return int(ibge_code), city_name

def disease_formatter(disease):
    disease = disease.replace('.', '').strip()
    disease_code = disease.split(' ')[0]
    disease_name = disease.replace(disease_code, '').strip()

    if len(disease_code) > 3:
        l = list(str(disease_code))
        l.insert(3, '.')
        disease_code = "".join(l)

    return float(disease_code), disease_name

def get_table_data_SIH(browser, name_content):
    soup = get_html_body(browser)
    tag_table = soup.find('table', {'class': 'tabdados'})

    tag_thead = tag_table.find('thead')
    tag_thead_tr = tag_thead.find_all('tr')
    tag_th = tag_thead_tr[1].find_all('th')
    
    header_table = []
    for th in tag_th:
        header_table.append(th.text.strip())

    tag_tbody = tag_table.find('tbody')
    tag_tbody_tr = tag_tbody.find_all('tr')
    data_final = []

    for tr in tag_tbody_tr:
        if tag_tbody_tr[0] == tr:
            pass
        else:
            tag_tbody_td = tr.find_all('td')
            data_partial = {}

            for index in range(len(header_table)-1):
                key = key_formatter(str(header_table[index]))
                value = value_formatter(tag_tbody_td[index].text)
                
                data_partial.update({key: value})
            
            ibge_code, city_name = ibge_code_city_formatter(data_partial['Município'])

            for i in data_partial:
                if i == 'Município':
                    pass
                else:
                    month = MONTHS[i.split('/')[1].lower()]
                    year = i.split('/')[0]
                    value = data_partial[i]

                    data_result = {
                        'codigo_ibge': ibge_code,
                        'nome_municipio': city_name.strip(),
                        'ano': int(year),
                        'mes': month,
                        'data_timeline': '{}-{}-01'.format(year, month),
                        name_content: value
                    }

                    data_final.append(data_result)

    return browser, data_final

def get_table_data_SINAN(browser, year, theme):
    soup = get_html_body(browser)
    tag_table = soup.find('table', {'class': 'tabdados'})

    tag_thead = tag_table.find('thead')
    tag_thead_tr = tag_thead.find_all('tr')
    tag_th = tag_thead_tr[1].find_all('th')
    
    header_table = []
    for th in tag_th:
        header_table.append(th.text.strip())

    tag_tbody = tag_table.find('tbody')
    tag_tbody_tr = tag_tbody.find_all('tr')
    data_final = []

    for tr in tag_tbody_tr:
        if tag_tbody_tr[0] == tr:
            pass
        else:
            tag_tbody_td = tr.find_all('td')

            data_partial = {}
            for index in range(len(header_table)-1):
                key = key_formatter(str(header_table[index]))
                value = value_formatter(tag_tbody_td[index].text)
                
                data_partial.update({key: value})
            
            ibge_code, city_name = ibge_code_city_formatter(data_partial['Município Residência'])

            for i in data_partial:
                if 'Município' in i:
                    pass
                else:
                    try:
                        month = MONTHS[i.lower()]
                        value = data_partial[i]

                        data_result = {
                            'codigo_ibge': ibge_code,
                            'nome_municipio': city_name.strip(),
                            'ano': int(year),
                            'mes': month,
                            'data_timeline': '{}-{}-01'.format(year, month),
                            'valor_{}'.format(theme): value
                        }

                        data_final.append(data_result)
                    except:
                        pass

    return browser, data_final

def get_table_data_SINASC(browser):
    soup = get_html_body(browser)
    tag_table = soup.find('table', {'class': 'tabdados'})

    tag_thead = tag_table.find('thead')
    tag_thead_tr = tag_thead.find_all('tr')
    tag_th = tag_thead_tr[1].find_all('th')
    
    header_table = []
    for th in tag_th:
        header_table.append(th.text.strip())

    tag_tbody = tag_table.find('tbody')
    tag_tbody_tr = tag_tbody.find_all('tr')
    data_final = []
    
    for tr in tag_tbody_tr:
        if tag_tbody_tr[0] == tr:
            pass
        else:
            tag_tbody_td = tr.find_all('td')

            data_partial = {}
            for index in range(len(header_table)-1):
                key = key_formatter(str(header_table[index]))
                value = value_formatter(tag_tbody_td[index].text)
                
                data_partial.update({key: value})
            
            ibge_code, city_name = ibge_code_city_formatter(data_partial['Município'])

            for i in data_partial:
                if i == 'Município':
                    pass
                else:
                    month = FULL_MONTHS[i.split('/')[0].lower()]
                    year = i.split('/')[1]
                    value = data_partial[i]

                    data_result = {
                        'codigo_ibge': ibge_code,
                        'nome_municipio': city_name.strip(),
                        'ano': int(year),
                        'mes': month,
                        'data_timeline': '{}-{}-01'.format(year, month),
                        'valor_nascimento': value
                    }

                    data_final.append(data_result)

    return browser, data_final

def get_table_data_SIM(browser, disease):
    soup = get_html_body(browser)
    tag_table = soup.find('table', {'class': 'tabdados'})

    tag_thead = tag_table.find('thead')
    tag_thead_tr = tag_thead.find_all('tr')
    tag_th = tag_thead_tr[1].find_all('th')
    
    header_table = []
    for th in tag_th:
        header_table.append(th.text.strip())

    tag_tbody = tag_table.find('tbody')
    tag_tbody_tr = tag_tbody.find_all('tr')
    data_final = []
    
    for tr in tag_tbody_tr:
        if tag_tbody_tr[0] == tr:
            pass
        else:
            tag_tbody_td = tr.find_all('td')

            data_partial = {}
            for index in range(len(header_table)-1):
                key = key_formatter(str(header_table[index]))
                value = value_formatter(tag_tbody_td[index].text)
                
                data_partial.update({key: value})
            
            ibge_code, city_name = ibge_code_city_formatter(data_partial['Município'])
            disease_code, disease_name = disease_formatter(disease)

            for i in data_partial:
                if i == 'Município':
                    pass
                else:
                    month = FULL_MONTHS[i.split('/')[0].lower()]
                    year = i.split('/')[1]
                    value = data_partial[i]

                    data_result = {
                        'codigo_ibge': ibge_code,
                        'nome_municipio': city_name.strip(),
                        'ano': int(year),
                        'mes': month,
                        'data_timeline': '{}-{}-01'.format(year, month),
                        'codigo_causa': disease_code,
                        'causa': disease_name,
                        'valor_mortalidade': value
                    }

                    data_final.append(data_result)

    return browser, data_final

def convert_to_csv(disease_data, filename):
    keys = disease_data[0].keys()
    with open('csv/{}.csv'.format(filename), 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(disease_data)