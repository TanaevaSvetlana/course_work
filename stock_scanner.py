import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QPlainTextEdit, QVBoxLayout
from PyQt5.QtWidgets import QInputDialog
from bs4 import BeautifulSoup as bs
import requests


# Функция для первого блока: "Показатели какой акции из двух лучше"
def best_share(x, y):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Upgrade-Insecure-Requests': '1', 'Cookie': 'v2=1495343816.182.19.234.142',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Referer': "http://finviz.com/quote.ashx?t="}
    p_e = [0, 0]
    p_s = [0, 0]
    p_b = [0, 0]
    debt_eq = [0, 0]
    roi = [0, 0]
    roe = [0, 0]
    roa = [0, 0]
    total_1 = 0
    total_2 = 0

    page = requests.get("http://finviz.com/quote.ashx?t=" + x, headers=headers)
    soup_ = bs(page.text, 'html.parser')
    p_e[0] = soup_.find(text='P/E').find_next(class_='snapshot-td2').text
    p_s[0] = soup_.find(text='P/S').find_next(class_='snapshot-td2').text
    p_b[0] = soup_.find(text='P/B').find_next(class_='snapshot-td2').text
    debt_eq[0] = soup_.find(text='Debt/Eq').find_next(class_='snapshot-td2').text
    roi[0] = soup_.find(text='ROI').find_next(class_='snapshot-td2').text
    roe[0] = soup_.find(text='ROE').find_next(class_='snapshot-td2').text
    roa[0] = soup_.find(text='ROA').find_next(class_='snapshot-td2').text

    page2 = requests.get("http://finviz.com/quote.ashx?t=" + y, headers=headers)
    soup_2 = bs(page2.text, 'html.parser')
    p_e[1] = soup_2.find(text='P/E').find_next(class_='snapshot-td2').text
    p_s[1] = soup_2.find(text='P/S').find_next(class_='snapshot-td2').text
    p_b[1] = soup_2.find(text='P/B').find_next(class_='snapshot-td2').text
    debt_eq[1] = soup_2.find(text='Debt/Eq').find_next(class_='snapshot-td2').text
    roi[1] = soup_2.find(text='ROI').find_next(class_='snapshot-td2').text
    roe[1] = soup_2.find(text='ROE').find_next(class_='snapshot-td2').text
    roa[1] = soup_2.find(text='ROA').find_next(class_='snapshot-td2').text

    # Подсчет коэффициентов и вывод той акции, у которой показатели лучше.
    if p_e[0] < p_e[1]:
        total_1 += 1
    elif p_e[1] < p_e[0]:
        total_2 += 1
    if p_s[0] < p_s[1]:
        total_1 += 1
    elif p_s[1] < p_s[0]:
        total_2 += 1
    if p_b[0] < p_b[1]:
        total_1 += 1
    elif p_b[1] < p_b[0]:
        total_2 += 1
    if debt_eq[0] < debt_eq[1]:
        total_1 += 1
    elif debt_eq[1] < debt_eq[0]:
        total_2 += 1
    if roi[0] > roi[1]:
        total_1 += 1
    elif roi[1] > roi[0]:
        total_2 += 1
    if roe[0] > roe[1]:
        total_1 += 1
    elif roe[1] > roe[0]:
        total_2 += 1
    if roa[0] > roa[1]:
        total_1 += 1
    elif roa[1] > roa[0]:
        total_2 += 1
    if total_1 > total_2:
        return f'Показатели акции {x} лучше'
    elif total_1 < total_2:
        return f'Показатели акции {y} лучше'
    else:
        return 'Показатели этих акций равны'


# Функция для третьего блока: "Средний показатель нужного коэффициента в выбранном секторе".
def avg_factor(x, y):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Upgrade-Insecure-Requests': '1', 'Cookie': 'v2=1495343816.182.19.234.142',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Referer': "http://finviz.com/quote.ashx?t="}

    factor_list = list()
    page_avg_factor = requests.get('https://www.gurufocus.com/industry_overview.php', headers=headers)
    soup_avg_factor = bs(page_avg_factor.text, 'html.parser')
    for td in soup_avg_factor.find(class_="text table_company").find_next(text=x).find_next(
            class_="text table_company").find_next(text='Overall').find_next().find_next_siblings():
        factor_list.append(td.text)
    if y == 'p_e':
        return f'Средний показатель {y} в секторе {x}: {factor_list[0]}'
    if y == 'p_s':
        return f'Средний показатель {y} в секторе {x}: {factor_list[6]}'
    if y == 'p_b':
        return f'Средний показатель {y} в секторе {x}: {factor_list[7]}'
    if y == 'dividend':
        return f'Средний показатель {y} в секторе {x}: {factor_list[12]}'
    if y == 'roe':
        return f'Средний показатель {y} в секторе {x}: {factor_list[18]}'
    if y == 'roa':
        return f'Средний показатель {y} в секторе {x}: {factor_list[19]}'
    if y == 'roc':
        return f'Средний показатель {y} в секторе {x}: {factor_list[20]}'
    if y == 'ev_ebitda':
        return f'Средний показатель {y} в секторе {x}: {factor_list[4]}'


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Сканер акций')
        self.button_1 = QPushButton(self)
        self.button_1.move(75, 100)
        self.button_1.resize(350, 100)
        self.button_1.setText('Чтобы начать работу нажмите на эту кнопку.')
        self.button_1.clicked.connect(self.run)
        self.show()

    def run(self):
        i, okBtnPressed = QInputDialog.getItem(self, "Действие с акциями",
                                               "Выберите нужный вариант",
                                               ('1. Показатели какой акции из двух лучше',
                                                '2. Топ 10 акций по выбранным показателям',
                                                '3. Средний показатель нужного коэффициента в выбранном секторе'),
                                               1, False)
        if okBtnPressed:
            if i == '1. Показатели какой акции из двух лучше':
                first, okBtnPressed2 = QInputDialog.getText(self, "Первая акция",
                                                            "Введите тикер первой акции")
                second, okBtnPressed3 = QInputDialog.getText(self, "Вторая акция",
                                                             "Введите тикер второй акции")

                vbox = QVBoxLayout()
                plainText = QPlainTextEdit()
                plainText.setPlaceholderText('')
                plainText.appendPlainText(best_share(first, second))
                plainText.setReadOnly(True)
                vbox.addWidget(plainText)
                self.setLayout(vbox)
                self.show()

            if i == '2. Топ 10 акций по выбранным показателям':
                from bs4 import BeautifulSoup as bs
                import requests

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                    'Upgrade-Insecure-Requests': '1', 'Cookie': 'v2=1495343816.182.19.234.142',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Referer': "http://finviz.com/quote.ashx?t="}

                sector, okBtnPressed = QInputDialog.getItem(self, "Секторы акций",
                                                            "Выберите нужный сектор",
                                                            ('Основные материалы - basicmaterials',
                                                             'Коммуникационные услуги - communicationservices',
                                                             'Потребительские вторичные товары - consumercyclical',
                                                             'Потребительские товары первой необходимости - consumerdefensive',
                                                             'Нефть и газ - energy',
                                                             'Финансы - financial',
                                                             'Здравоохранение - healthcare',
                                                             'Промышленность - industrials',
                                                             'Недвижимость - realestate',
                                                             'Технологии - technology',
                                                             'Коммунальные услуги - utilities'),
                                                            1, False)
                factor, okBtnPressed = QInputDialog.getItem(self, "Показатели акций",
                                                            "Выберите нужный показатель",
                                                            ('pe',
                                                             'price',
                                                             'change',
                                                             'volume',
                                                             'ticker'),
                                                            1, False)
                if okBtnPressed:
                    if sector == 'Основные материалы - basicmaterials':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'basicmaterials' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе basicmaterials,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Коммуникационные услуги - communicationservices':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'communicationservices' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе communicationservices,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Потребительские вторичные товары - consumercyclical':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'consumercyclical' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе consumercyclical,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Потребительские товары первой необходимости - consumerdefensive':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'consumerdefensive' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе consumerdefensive,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Нефть и газ - energy':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'energy' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе energy,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Финансы - financial':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'financial' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе financial,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Здравоохранение - healthcare':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'healthcare' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе healthcare,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Промышленность - industrials':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'industrials' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе industrials,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Недвижимость - realestate':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'realestate' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе realestate,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Технологии - technology':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'technology' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе technology,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

                    if sector == 'Коммунальные услуги - utilities':
                        list_share = list()
                        page_top = requests.get(
                            "https://finviz.com/screener.ashx?v=111&f=geo_usa,sec_" + 'utilities' + '&o=' + factor,
                            headers=headers)
                        soup_top = bs(page_top.text, 'html.parser')
                        for i in range(1, 11):
                            list_share.append(str(i) + '.   ' + soup_top.find(text=i).find_next(
                                class_="screener-link-primary").text)

                        vbox = QVBoxLayout()
                        plainText = QPlainTextEdit()
                        plainText.appendPlainText(f'Топ-10 акций в секторе utilities,  '
                                                  f'сортированных по возрастанию {factor}: ')
                        for i in list_share:
                            plainText.appendPlainText(i)
                        plainText.setReadOnly(True)
                        vbox.addWidget(plainText)
                        self.setLayout(vbox)
                        self.show()

            if i == '3. Средний показатель нужного коэффициента в выбранном секторе':

                sector_avg, okBtnPressed = QInputDialog.getItem(self, "Секторы акций",
                                                                "Выберите нужный сектор",
                                                                ('Basic Materials (Основные материалы)',
                                                                 'Consumer Cyclical (Потребительские вторичные товары)',
                                                                 'Financial Services (Финансовые услуги)',
                                                                 'Real Estate (Недвижимость)',
                                                                 'Consumer Defensive (Потребительские товары первой необходимости)',
                                                                 'Healthcare (Здравоохранение)',
                                                                 'Utilities (Коммунальные услуги)',
                                                                 'Communication Services (Услуги связи)',
                                                                 'Energy (Нефть и газ)',
                                                                 'Industrials (Промышленность)',
                                                                 'Technology (Технологии)'),
                                                                1, False)
                factor, okBtnPressed = QInputDialog.getItem(self, "Показатели акций",
                                                            "Выберите нужный показатель",
                                                            ('p_e',
                                                             'p_s',
                                                             'p_b',
                                                             'roe',
                                                             'roa',
                                                             'roc',
                                                             'ev_ebitda'),
                                                            1, False)
                if okBtnPressed:
                    if sector_avg == 'Basic Materials (Основные материалы)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Basic Materials', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Basic Materials', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Basic Materials', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Basic Materials', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Basic Materials', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Basic Materials', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Basic Materials', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Consumer Cyclical (Потребительские вторичные товары)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Consumer Cyclical', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Consumer Cyclical', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Consumer Cyclical', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Consumer Cyclical', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Consumer Cyclical', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Consumer Cyclical', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Consumer Cyclical', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Financial Services (Финансовые услуги)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Financial Services', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Financial Services', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Financial Services', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Financial Services', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Financial Services', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Financial Services', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Financial Services', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Real Estate (Недвижимость)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Real Estate', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Real Estate', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Real Estate', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Real Estate', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Real Estate', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Real Estate', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Real Estate', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Consumer Defensive (Потребительские товары первой необходимости)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Consumer Defensive', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Consumer Defensive', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Consumer Defensive', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Consumer Defensive', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Consumer Defensive', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Consumer Defensive', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Consumer Defensive', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Healthcare (Здравоохранение)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Healthcare', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Healthcare', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Healthcare', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Healthcare', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Healthcare', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Healthcare', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Healthcare', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Utilities (Коммунальные услуги)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Utilities', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Utilities', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Utilities', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Utilities', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Utilities', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Utilities', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Utilities', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Communication Services (Услуги связи)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Communication Services', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Communication Services', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Communication Services', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Communication Services', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Communication Services', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Communication Services', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Communication Services', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Energy (Нефть и газ)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Energy', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Energy', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Energy', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Energy', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Energy', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Energy', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Energy', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Industrials (Промышленность)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Industrials', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Industrials', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Industrials', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Industrials', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Industrials', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Industrials', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Industrials', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()

                    if sector_avg == 'Technology (Технологии)':
                        if okBtnPressed:
                            vbox = QVBoxLayout()
                            plainText = QPlainTextEdit()
                            if factor == 'p_e':
                                plainText.appendPlainText(avg_factor('Technology', factor))
                            if factor == 'p_s':
                                plainText.appendPlainText(avg_factor('Technology', factor))
                            if factor == 'p_b':
                                plainText.appendPlainText(avg_factor('Technology', factor))
                            if factor == 'roe':
                                plainText.appendPlainText(avg_factor('Technology', factor))
                            if factor == 'roa':
                                plainText.appendPlainText(avg_factor('Technology', factor))
                            if factor == 'roc':
                                plainText.appendPlainText(avg_factor('Technology', factor))
                            if factor == 'ev_ebitda':
                                plainText.appendPlainText(avg_factor('Technology', factor))
                            plainText.setReadOnly(True)
                            vbox.addWidget(plainText)
                            self.setLayout(vbox)
                            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
