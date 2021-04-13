import pytest
import html5lib
import pandas as pd
import time
import threading
import csv
import pdfkit
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen, Request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

WARNING = '\033[93m'
WHITE = '\033[0m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'

options = EdgeOptions()
options.use_chromium = True
# Sin abrirnavegador
options.headless = True
options.add_argument('disable-gpu')
options.add_argument('no-sandbox')
driver = Edge(options=options, executable_path='msedgedriver.exe')
vars = {}

USERNAME = 'ohernandez'
PASSWORD = 'os23valdo1'
EMAIL = 'osvaldo.hdz.m@outlook.com'


def wait_for_window(timeout=2):
    time.sleep(round(timeout / 1000))
    wh_now = driver.window_handles
    wh_then = vars["window_handles"]
    if len(wh_now) > len(wh_then):
        return set(wh_now).difference(set(wh_then)).pop()


def access_capitales():
    try:
        print('\t' + WARNING + "Accediendo a capitales..." + WHITE)
        driver.get('https://www.retoactinver.com/RetoActinver/#/capitales')
        driver.refresh()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="botonCerrar"]/mat-icon').click()
        driver.find_element_by_xpath(
            '/html/body/app-root/block-ui/app-paginas/app-layout-principal/mat-sidenav-container/mat-sidenav-content/div[2]/div/app-capitales/div/div[2]/mat-card/mat-tab-group/div/mat-tab-body[1]/div/div/div/app-table/div/gt-column-settings/div/div/generic-table/table')
    except:
        print("Iniciando sesión...")
        driver.get('https://www.retoactinver.com/RetoActinver/#/login')
        driver.refresh()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="botonCerrar"]/mat-icon').click()
        user_input = driver.find_element_by_id('mat-input-0')
        user_input.send_keys(USERNAME)
        password_input = driver.find_element_by_id('mat-input-1')
        password_input.send_keys(PASSWORD)
        login_button = driver.find_element_by_xpath(
            "/html/body/app-root/block-ui/app-login/div/form/button[1]/span")
        login_button.click()


def retrieve_data_reto_capitales():
    try:
        print('\t' + WARNING + "Accediendo a datos de tabla de capitales..." + WHITE)
        driver.get('https://www.retoactinver.com/RetoActinver/#/capitales')
        driver.refresh()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="botonCerrar"]/mat-icon').click()
        time.sleep(6)
        driver.find_element_by_xpath(
            '//*[@id="mat-select-1"]/div/div[1]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="mat-option-1"]').click()
        driver.find_element_by_xpath(
            '//*[@id="mat-tab-content-0-0"]/div/div/div/app-table/div/gt-column-settings/div/div/generic-table/table/thead[1]/tr/th[6]/span').click()
        hoursTable = driver.find_element_by_xpath(
            '/html/body/app-root/block-ui/app-paginas/app-layout-principal/mat-sidenav-container/mat-sidenav-content/div[2]/div/app-capitales/div/div[2]/mat-card/mat-tab-group/div/mat-tab-body[1]/div/div/div/app-table/div/gt-column-settings/div/div/generic-table/table').get_attribute("outerHTML")
        dfs = pd.read_html(hoursTable)
        df = dfs[0]
        df.drop(['Sort:', 'Unnamed: 1', 'Información', 'Precio de Compra', 'Volumen de Venta',
                 '% Variación', 'Volumen Compra', 'Precio de Venta'], axis=1, inplace=True)
        df.rename(columns={'Precio': 'Variación'}, inplace=True)
        df['Variación'] = df['Variación'].str.replace('% Variación', '')
        df['Variación'] = df['Variación'].str.replace('%', '')
        df.rename(columns={'Emisora': 'Precio'}, inplace=True)
        df['Precio'] = df['Precio'].str.replace('Precio', '')
        df.rename(columns={'Categorias': 'Emisora'}, inplace=True)
        df['Emisora'] = df['Emisora'].str.replace('Emisora', '')
        df['Emisora'] = df['Emisora'].str.replace(' *', '')
        df['Emisora'] = df['Emisora'].str.replace('*', '')
        df['Datetime'] = datetime.now().strftime("%x %X")
        print(df.head(5))
        df.to_csv('top_dia.csv', index=False, header=True, encoding="utf-8")
    except:
        login_actinver()
        retrieve_data_reto_capitales()


def login_actinver():
    try:
        print('\t' + WARNING + "Iniciando sesión..." + WHITE)
        # driver.get('https://www.retoactinver.com/RetoActinver/#/login')
        driver.refresh()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="botonCerrar"]/mat-icon').click()
        user_input = driver.find_element_by_id('mat-input-0')
        user_input.send_keys(USERNAME)
        password_input = driver.find_element_by_id('mat-input-1')
        password_input.send_keys(PASSWORD)
        login_button = driver.find_element_by_xpath(
            "/html/body/app-root/block-ui/app-login/div/form/button[1]/span")
        login_button.click()
    except:
        session_handle()


def retrieve_data_reto_portafolio():
    # while True:
    print('\t' + WARNING + "Accediendo a datos de tabla de portafolio..." + WHITE)
    driver.get('https://www.retoactinver.com/RetoActinver/#/portafolio')
    driver.refresh()
    time.sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="botonCerrar"]').click()
    hoursTable = driver.find_element_by_xpath(
        '//*[@id="tpm"]/app-portafolio/div/div[3]/mat-card/app-table/div/gt-column-settings/div/div/generic-table/table').get_attribute("outerHTML")
    dfs = pd.read_html(hoursTable)
    df = dfs[0]
    df = df[['Categorias', 'Emisora', 'Títulos',
             'Precio Actual', 'Variación $']]
    df.rename(columns={'Variación $': 'Variación %'}, inplace=True)
    df['Variación %'] = df['Variación %'].str.replace('% Variación', '')
    df['Variación %'] = df['Variación %'].str.replace('%', '')
    df.rename(columns={'Precio Actual': 'Valor actual'}, inplace=True)
    df['Valor actual'] = df['Valor actual'].str.replace('Valor Actual', '')
    df.rename(columns={'Títulos': 'Costo de compra'}, inplace=True)
    df['Costo de compra'] = df['Costo de compra'].str.replace(
        'Valor del Costo', '')
    df.rename(columns={'Emisora': 'Títulos'}, inplace=True)
    df['Títulos'] = df['Títulos'].str.replace('Títulos', '')
    df.rename(columns={'Categorias': 'Emisora'}, inplace=True)
    df['Emisora'] = df['Emisora'].str.replace('Emisora', '')
    df['Emisora'] = df['Emisora'].str.replace(' *', '')
    df['Emisora'] = df['Emisora'].str.replace('*', '')
    df['Datetime'] = datetime.now().strftime("%x %X")
    print(df.head(10))
    df.to_csv('actinver_portfolio.csv', index=False,
              header=True, encoding="utf-8")


def session_handle():
    try:
        print('\t' + WARNING + "Cerrando sesión anterior e iniciando nueva..." + WHITE)
        time.sleep(3)
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/mat-dialog-container/app-destroy-session/mat-dialog-actions/div[1]/button").click()
        nickname_input = driver.find_element_by_xpath(
            '//*[@id="mat-input-2"]')
        nickname_input.send_keys(USERNAME)
        email_input = driver.find_element_by_xpath(
            '//*[@id="mat-input-3"]')
        email_input.send_keys(EMAIL)
        driver.find_element_by_xpath(
            '//*[@id="mat-dialog-1"]/app-destroy-session/mat-dialog-actions/div/button/span').click()
        login_button = driver.find_element_by_xpath(
            "/html/body/app-root/block-ui/app-login/div/form/button[1]/span")
        login_button.click()
        driver.implicitly_wait(45)
        driver.execute_script("window.open('');")
        # Switch to the new window
        driver.switch_to.window(driver.window_handles[1])
    except:
        print("Sesión ya establecida...")


def investig_retrieve_data():
    print('\t' + WARNING + "Calculando análisis simple..." + WHITE)
    driver.get("https://www.investing.com/")
    driver.find_element(By.LINK_TEXT, "Sign In").click()
    time.sleep(2)
    vars["window_handles"] = driver.window_handles
    driver.find_element_by_xpath('//*[@id="customBtn1"]').click()
    vars["win1742"] = wait_for_window(2000)
    vars["root"] = driver.current_window_handle
    driver.switch_to.window(vars["win1742"])
    driver.find_element(By.ID, "identifierId").send_keys(
        "osvaldo.hdz.m@outlook.com")
    driver.find_element(By.ID, "identifierId").send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys("os23valdo1")
    driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
    driver.switch_to.window(vars["root"])
    time.sleep(8)
    driver.find_element_by_xpath('//*[@id="portfolioTopBarBtn"]').click()
    time.sleep(6)
    driver.find_element(By.LINK_TEXT, "Reto Actinver").click()
    driver.find_element(By.LINK_TEXT, "Performance").click()
    time.sleep(3)
    table = driver.find_element_by_xpath(
        '/html/body/div[5]/section/div[7]/div[7]/div[2]/div[2]/div/table').get_attribute("outerHTML")
    dfs = pd.read_html(table)
    df = dfs[0]
    df.drop(['Unnamed: 0', 'Unnamed: 8'], axis=1, inplace=True)
    df['Datetime'] = datetime.now().strftime("%x %X")
    print(df)
    df.to_csv('analisis_tecnico_performance.csv',
              index=False, header=True, encoding="utf-8")

    driver.find_element(By.CSS_SELECTOR, "#technical > a").click()
    time.sleep(3)
    table = driver.find_element_by_xpath(
        '/html/body/div[5]/section/div[7]/div[7]/div[2]/div[2]/div/table').get_attribute("outerHTML")
    dfs = pd.read_html(table)
    df = dfs[0]
    df.drop(['Unnamed: 0', 'Unnamed: 10'], axis=1, inplace=True)
    df['Datetime'] = datetime.now().strftime("%x %X")
    print(df)
    df.to_csv('analisis_tecnico_algoritmo.csv',
              index=False, header=True, encoding="utf-8")


def news_analisys():
    # Parameters
    n = 3  # the # of article headlines displayed per ticker
    tickers = ['AAPL', 'TSLA', 'AMZN']

    for ticker in tickers:
        print('\n')
        print('Recent News Headlines for {}: '.format(ticker))
        driver.get("https://mx.investing.com/search/?q=" + ticker)
        driver.find_element_by_xpath(
                '//*[@id="searchPageResultsTabs"]/*/a[contains(text(), "Noticias")]').click()
        for x in range(1, n):
            print(driver.find_element_by_xpath('//*[@id="fullColumn"]/div/div[4]/div[3]/div/div['+str(x)+']/div/p').get_attribute('innerHTML')+' '+driver.find_element_by_xpath('//*[@id="fullColumn"]/div/div[4]/div[3]/div/div['+str(x)+']/div/div/time').get_attribute('innerHTML'))
   

    # Get Data
    finwiz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    for ticker in tickers:
        url = finwiz_url + ticker
        req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
        resp = urlopen(req)
        html = BeautifulSoup(resp, features="lxml")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table

    try:
        for ticker in tickers:
            df = news_tables[ticker]
            df_tr = df.findAll('tr')

            print('\n')
            print('Recent News Headlines for {}: '.format(ticker))

            for i, table_row in enumerate(df_tr):
                a_text = table_row.a.text
                td_text = table_row.td.text
                td_text = td_text.strip()
                print(a_text, '(', td_text, ')')
                if i == n-1:
                    break
    except KeyError:
        pass

    # Iterate through the news
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text()
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                timer = date_scrape[0]

            else:
                date = date_scrape[0]
                timer = date_scrape[1]

            ticker = file_name.split('_')[0]

            parsed_news.append([ticker, date, timer, text])

    # Sentiment Analysis
    analyzer = SentimentIntensityAnalyzer()

    columns = ['Ticker', 'Date', 'Time', 'Headline']
    news = pd.DataFrame(parsed_news, columns=columns)
    scores = news['Headline'].apply(analyzer.polarity_scores).tolist()

    df_scores = pd.DataFrame(scores)
    news = news.join(df_scores, rsuffix='_right')

    # View Data
    news['Date'] = pd.to_datetime(news.Date).dt.date

    unique_ticker = news['Ticker'].unique().tolist()
    news_dict = {name: news.loc[news['Ticker'] == name]
                 for name in unique_ticker}

    values = []
    for ticker in tickers:
        dataframe = news_dict[ticker]
        dataframe = dataframe.set_index('Ticker')
        dataframe = dataframe.drop(columns=['Headline'])
        print('\n')
        print(dataframe.head())

        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)

    df = pd.DataFrame(list(zip(tickers, values)), columns=[
                      'Ticker', 'Mean Sentiment'])
    df = df.set_index('Ticker')
    df = df.sort_values('Mean Sentiment', ascending=False)
    print('\n')
    print(df)


def analisys_result():
    print('\n\n\t' + OKGREEN + "RESULTADO DE ANALISIS:")

    df = pd.read_csv('analisis_tecnico_algoritmo.csv')
    print(OKGREEN + df)
    df = df.loc[(df['30 Minutes'] == 'Strong Buy') & (df['5 Minutes'] == 'Strong Buy') & (df['15 Minutes'] == 'Strong Buy') & (
        df['Hourly'] == 'Strong Buy') & (df['Daily'] == 'Strong Buy') & (df['Weekly'] == 'Strong Buy') & (df['Monthly'] == 'Strong Buy')].copy()
    print(df)
    names = df['Name'].tolist()
    df = df[['Name']]
    df['Precio estimado de compra $'] = "-"
    df['Precio estimado de venta $'] = "-"
    df['Variacion estimada %'] = "-"
    df['StockName'] = "-"
    df['Datetime'] = datetime.now().strftime("%x %X")

    index_for = 0
    for stock_name in names:
        time.sleep(3)
        driver.get("https://mx.investing.com/search/?q=" + stock_name)
        driver.find_element_by_xpath(
            '/html/body/div[5]/section/div/div[2]/div[2]/div[2]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '/html/body/div[5]/section/div/div[3]/div[3]/div/*/span[contains(text(), "México")]').click()
        stock_name_found = driver.find_element_by_xpath(
            '/html/body/div[5]/section/div[7]/h2 ').get_attribute("innerText").replace('Panorama ', '')
        print(stock_name_found)

        driver.find_element_by_xpath(
            '//*[@id="pairSublinksLevel1"]/*/a[contains(text(), "Técnico")]').click()
        time.sleep(3)
        driver.find_element_by_xpath(
            '//*[@id="timePeriodsWidget"]/li[6]').click()
        time.sleep(2)
        table = driver.find_element_by_xpath(
            '/html/body/div[5]/section/div[10]/table').get_attribute("outerHTML")
        dfsb = pd.read_html(table)
        dfb = dfsb[0]
        print(dfb)
        expected_price_buy = (float(dfb.at[0, 'S2'])+float(dfb.at[0, 'S1']))/2
        print(format(expected_price_buy, '.2f'))
        expected_price_sell = (
            float(dfb.at[0, 'R2'])+float(dfb.at[0, 'R1']))/2
        print(format(expected_price_sell, '.2f'))
        expected_var = ((expected_price_sell/expected_price_buy)-1)*100
        print(format(expected_var, '.2f'))

        df.iat[index_for, 1] = format(expected_price_buy, '.2f')
        df.iat[index_for, 2] = format(expected_price_sell, '.2f')
        df.iat[index_for, 3] = format(expected_var, '.2f')
        df.iat[index_for, 4] = stock_name_found
        index_for += 1

    print(OKGREEN + df)
    print('\n' + WHITE)
    f = open('result.html', 'w')
    a = df.to_html()
    f.write(a)
    f.close()

    pdfkit.from_file('result.html', 'result.pdf')


def retrieve_top_reto():
    print('\t' + WARNING + "Accediendo a pulso del reto..." + WHITE)
    time.sleep(3)
    driver.get('https://www.retoactinver.com/RetoActinver/#/pulso')
    driver.refresh()
    time.sleep(3)
    driver.find_element_by_xpath(
        '//*[@id="botonCerrar"]/mat-icon').click()
    time.sleep(3)
    driver.find_element(
        By.CSS_SELECTOR, ".col-4:nth-child(3) > .btn-filtros").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".mat-form-field-infix").click()
    driver.find_element(By.CSS_SELECTOR, "#mat-option-5 > span").click()
    time.sleep(3)
    table = driver.find_element_by_xpath(
        '/html/body/app-root/block-ui/app-paginas/app-layout-principal/mat-sidenav-container/mat-sidenav-content/div[2]/div/pulso-reto/div/div[4]/mat-card/mat-card-content/mat-tab-group/div/mat-tab-body[1]/div/div/tabla-alzas-bajas/div/div/app-table/div/gt-column-settings/div/div/generic-table/table').get_attribute("outerHTML")
    dfs = pd.read_html(table)
    df = dfs[0]
    df.drop(['% de Variación'], axis=1, inplace=True)
    print(df)
    df.rename(columns={'Precio Actual': 'Variación'}, inplace=True)
    df['Variación'] = df['Variación'].str.replace('% de Variación ', '')
    df['Variación'] = df['Variación'].str.replace('%', '')
    df.rename(columns={'Emisora': 'Precio Historico'}, inplace=True)
    df['Precio Historico'] = df['Precio Historico'].str.replace(
        'Historico', '')
    df.rename(columns={'Historico': 'Precio Actual'}, inplace=True)
    df['Precio Actual'] = df['Precio Actual'].str.replace('Precio Actual', '')
    df.rename(columns={'Sort:': 'Emisora'}, inplace=True)
    df['Emisora'] = df['Emisora'].str.replace('Emisora', '')
    df['Emisora'] = df['Emisora'].str.replace(' *', '')
    print(df)
    df.to_csv('top_reto.csv', index=False, header=True, encoding="utf-8")


access_capitales()
session_handle()
retrieve_top_reto()
retrieve_data_reto_capitales()
retrieve_data_reto_portafolio()
investig_retrieve_data()
analisys_result()
news_analisys()
driver.close()
