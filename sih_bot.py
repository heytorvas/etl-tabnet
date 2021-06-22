from bot import *
from slugify import slugify

URL = 'http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/nrmg.def'
content_list = get_content_select(URL)

for content in content_list:
    browser = get_browser(URL)
    row_filter = set_filter(browser, 'L', 'Município')
    col_filter = set_filter(row_filter, 'C', 'Ano/mês atendimento')
    cont_filter = set_content_filter(col_filter, 'I', content)

    year_filter = set_year_filter(col_filter)
    cause_filter = set_cause_filter_SIH(col_filter, 'IX. Doenças do aparelho circulatório')
    sleep(60)

    name_content = str(slugify(content)).replace('-', '_')

    table_data, data = get_table_data_SIH(cause_filter, name_content)
    sleep(2)
    table_data.quit()

    convert_to_csv(data, 'sih_{}'.format(name_content))
    print(content)