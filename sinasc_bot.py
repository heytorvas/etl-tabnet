from bot import *

URL = 'http://tabnet.saude.mg.gov.br/deftohtm.exe?def/nasc/nascr.def'

browser = get_browser(URL)
row_filter = set_filter(browser, 'L', 'Município')
col_filter = set_filter(row_filter, 'C', 'Mês/Ano do Nascimento')
year_filter = set_year_filter(col_filter)
year_filter.find_element_by_xpath('/html/body/center/div/form/div[4]/div[2]/div[2]/input[1]').click()

table_data, data = get_table_data_SINASC(year_filter)
sleep(2)
table_data.quit()

convert_to_csv(data, 'sinasc')