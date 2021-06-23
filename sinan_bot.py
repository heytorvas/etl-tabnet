from bot import *
from time import sleep
from slugify import slugify

def get_diseases_list():
    URL = 'http://vigilancia.saude.mg.gov.br/index.php/informacoes-de-saude/informacoes-de-saude-tabnet-mg/'

    page = requests.get(URL).text
    soup = BeautifulSoup(page, 'html.parser')

    diseases = soup.find_all('div', {'class': 'su-tabs-pane su-clearfix'})[2]
    panes = diseases.find_all('div', {'class': 'su-spoiler su-spoiler-style-fancy su-spoiler-icon-plus su-spoiler-closed'})

    diseases_list = []
    for disease in panes:
        title = str(disease.find('div', {'class': 'su-spoiler-title'}).text).strip()
        links = disease.find_all('a')
        for l in links:
            if l.text == 'Local de residência':
                diseases_list.append({'title': title, 'link': l.get('href')})

    return diseases_list

diseases_list = get_diseases_list()
#diseases_list = [{'title': 'Botulismo', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/botulismo_r.def'}, {'title': 'Chikungunya', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/chikungunya_r.def'}, {'title': 'Coqueluche', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/coque_r.def'}, {'title': 'Dengue', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/dengue_r.def'}, {'title': 'Difteria', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/difteria_r.def'}, {'title': 'Doença de Chagas Aguda', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/chagas_r.def'}, {'title': 'Doenças Exantemáticas (Sarampo e Rubéola)', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/exant_r.def'}, {'title': 'Esquistossomose', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/esquistossomose_r.def'}, {'title': 'Febre amarela', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/famarnet_r.def'}, {'title': 'Hanseníase', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/hans_r.def'}, {'title': 'Hepatites virais', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/hepatites_r.def'}, {'title': 'Intoxicação exógena', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/iexogena_r.def'}, {'title': 'Leishmaniose Tegumentar Americana', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/leishteg_r.def'}, {'title': 'Leishmaniose Visceral', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/leishvisc_r.def'}, {'title': 'Malária', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/malaria_r.def'}, {'title': 'Sífilis congênita', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/sifcong_r.def'}, {'title': 'Sífilis em gestante', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/sifgest_r.def'}, {'title': 'Tuberculose', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/tuberculose_r.def'}, {'title': 'Violência Interpessoal / Autoprovocada', 'link': 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/agravos/violencia_r.def'}]

for disease in diseases_list:
    # for diseases
    URL = disease['link']
    theme = slugify(disease['title'])
    theme = theme.replace('-', '_')
    years = get_size_year_SINAN(URL)
    disease_data = []
    for year in years:
        # for year
        browser = get_browser(URL)
        row_filter = set_filter_SINAN(browser, 'L', 'Município')
        col_filter = set_col_filter_SINAN(browser, 'C')
        year_filter = set_year_filter_SINAN(browser, year)
        year_filter.find_element_by_xpath('/html/body/center/div/form/div[4]/div[2]/div[2]/input[1]').click()

        sleep(10)
        
        try:
            table_data, data = get_table_data_SINAN(year_filter, year, theme)
        
            for i in data:
                disease_data.append(i)

            table_data.quit()
        except:
            pass

        print('{} | {}'.format(theme, year))

    convert_to_csv(disease_data, 'sinan_{}'.format(theme))