from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import numpy as np

def fieldName(column, detail):
    if column == "036Y002":
        if detail == "0000001":
            column = "won_dollor"
        elif detail == "0000002":
            column = "won_yen"
        else:
            column = "won_euro"
    else:
        column = "dollor_euro"

    return str(column)

# 환율(원달러, 원엔, 원유료, 달러유로)
def exchangeRate(apiKey, startPage, endPage, code, freq, startDate, endDate, detailCode):
    url = 'https://ecos.bok.or.kr/api/StatisticSearch/%s/xml/kr/%s/%s/%s/%s/%s/%s/%s/'\
          %(apiKey, startPage, endPage, code, freq, startDate, endDate, detailCode)
    row = requests.get(url)
    allData = row.text

    xml = BeautifulSoup(allData, 'html.parser')

    row_date = xml.find_all("row")

    dateList = []
    valueList = []

    for item in row_date:
        dateStr = item.time.text
        value = item.data_value.text
        try:
            value = float(value)
        except:
            value = np.nan

        dateList.append(datetime.datetime.strptime(dateStr, '%Y%m%d'))
        valueList.append(value)

    df = pd.DataFrame(index = dateList)
    df['%s'%(fieldName(code, detailCode))] = valueList
    df.to_csv('exchangeRate.csv')

    return df

def valueOfData(apiKey, startPage, endPage, code, freq, startDate, endDate, detail):
    url = 'https://ecos.bok.or.kr/api/StatisticSearch/%s/xml/kr/%s/%s/%s/%s/%s/%s/%s/' \
          % (apiKey, startPage, endPage, code, freq, startDate, endDate, detail)
    row = requests.get(url)
    allData = row.text

    xml = BeautifulSoup(allData, 'html.parser')

    row_date = xml.find_all("row")

    dateList = []
    valueList = []

    for item in row_date:
        dateStr = item.time.text
        value = item.data_value.text

        try:
            value = float(value)
        except:
            value = np.nan

        dateList.append(datetime.datetime.strptime(dateStr, '%Y%m'))
        valueList.append(value)
    df = pd.DataFrame(index=dateList)
    df['%s'%(detail)] = valueList
    return df

# 경기종합지수 (선행, 동행, 후행)
def compositeIndexOfBusinessIndicators(apiKey, startPage, endPage, code, freq, startDate, endDate):
    detail = ['I16A', 'I16B', 'I16C']
    data = pd.DataFrame()
    result = pd.DataFrame()

    for i in range(0, len(detail)):
        result = valueOfData(apiKey, startPage, endPage, code, freq, startDate, endDate, detail[i])
        if i == 0:
            data = result
        else:
            data = pd.merge(result, data, left_index=True, right_index=True, how='outer')
    data.to_csv('ciobi.csv')


if __name__ == "__main__":

    # (startPage, endPage, code, freq, startDate, endDate, detailCode)
    apiKey = "PJRC8Q0ML86Q2MIS8DBA"

    # 원/달러 = 1970년 1월 5일부터  #036Y001, 0000001
    # 원/엔 = 1970년 4월 1일부터  #036Y001, 0000002
    # 원/유로 = 1994년 4월 11일부터  #036Y001, 0000003
    # 달러/유로 = 1994년 4월 11일부터  #036Y002, 0000003
    # df_ecos_exchange = exchangeRate(apiKey, '1', '100000', '036Y002', 'DD', '19700105', '20220120', '0000002')

    # 경기 종합 지수 (선행, 동행, 후행) = 1970년 1월 부터  #085Y026, [I16A, I16B, I16C]
    df_ecos_composite = compositeIndexOfBusinessIndicators(apiKey, '1', '100000', '085Y026', 'MM', '197001', '202201')

    # 소비자동향조사 소비지출전망CSI (~2008년 이전 : 분기, 2008년 이후 ~ : 월)
    # df_ecos_spending_plan = spendingPlan(apiKey, '1', '100000', '085Y026', 'MM', '197001', '202201')



