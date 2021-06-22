from bot import *

URL = 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/obitos/geralr.def'

diseases_list = ['. 066 Febre reumát aguda e doen reum crôn coração', '. 067 Doenças hipertensivas', '... 068.1 Infarto agudo do miocárdio', '. 069 Outras doenças cardíacas', '. 070 Doenças cerebrovasculares', '. 071 Aterosclerose', '. 072 Rest doenças do aparelho circulatório']
disease_data = []

for disease in diseases_list:
    browser = get_browser(URL)
    row_filter = set_filter(browser, 'L', 'Município')
    col_filter = set_filter(row_filter, 'C', 'Mês/Ano do Óbito')
    year_filter = set_year_filter(col_filter)
    cause_filter = set_cause_filter_SIM(year_filter, disease)
    
    sleep(2)

    table_data, data = get_table_data_SIM(cause_filter, disease)

    for i in data:
        disease_data.append(i)

    table_data.quit()
    print(disease)

convert_to_csv(disease_data, 'sim')