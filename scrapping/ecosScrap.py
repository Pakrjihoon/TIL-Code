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
        if(len(startDate) == 4):
            dateList.append(dateStr)
        else:
            if(len(dateStr) == 4):
                dateList.append(datetime.datetime.strptime(dateStr, '%Y'))
            else:
                dateList.append(datetime.datetime.strptime(dateStr, '%Y%m'))

        valueList.append(value)
    df = pd.DataFrame(index=dateList)
    df['%s'%(detail)] = valueList
    return df

# 공통 호출 함수 (기간, 통계코드 및 하위 depth 코드 사용으로 사용)
def commonCall(apiKey, startPage, endPage, code, freq, startDate, endDate):
    #detail = ['I16A', 'I16B', 'I16C']  # 경기종합지수 (선행, 동행, 후행)
    #detail = ['AI1AA', 'AI1AB', 'AI1AF']  # 경제 성장률 (경제성장률, 민간소비증감률, 국내총투자율)
    #detail = ['AI1AJ', 'AI1AK', 'AI1AH', 'AI1AI']  # 고용지표 (실업률, 고용률, 제조업 평균가동률, 제조업 재고율)
    #detail = ['AI1BB', 'AI1BA', 'AI1BC', 'AI1BF', 'AI1BD', 'AI1BE']  # 물가지수 (소비자/생산자 물가지수, 근원인플레이션율, 주택매매 가격등락률, 수출/수입 물가지수)
    #detail = ['AI1CA', 'AI1CB', 'AI1CE', 'AI1CF']  # 통화금융증권 (M1, M2, CD(91일), 국고채(3년))
    #detail = ['AI1DC', 'AI1DA', 'AI1DAA', 'AI1DAB']  # 국제수지 무역 (외환보유액, 경상수지, 상품수지, 서비스수지)
    #detail = ['AI1DC', 'AI1DA', 'AI1CH']  # 국내총생산 (외환보유액, 경상수지, 가계신용잔액)
    detail = ['1010101']  # 국내총생산 (GDP)
    data = pd.DataFrame()
    result = pd.DataFrame()

    for i in range(0, len(detail)):
        result = valueOfData(apiKey, startPage, endPage, code, freq, startDate, endDate, detail[i])
        if i == 0:
            data = result
        else:
            data = pd.merge(result, data, left_index=True, right_index=True, how='outer')
    data.to_csv('gdp2.csv')


if __name__ == "__main__":

    # (startPage, endPage, code, freq, startDate, endDate, detailCode)
    apiKey = "PJRC8Q0ML86Q2MIS8DBA"

    # 원/달러 = 1970년 1월 5일부터  #036Y001, 0000001
    # 원/엔 = 1970년 4월 1일부터  #036Y001, 0000002
    # 원/유로 = 1994년 4월 11일부터  #036Y001, 0000003
    # 달러/유로 = 1994년 4월 11일부터  #036Y002, 0000003
    # df_ecos_exchange = exchangeRate(apiKey, '1', '100000', '036Y002', 'DD', '19700105', '20220120', '0000002')

    # 경기 종합 지수 (선행, 동행, 후행) = 1970년 1월 ~  #085Y026, [I16A, I16B, I16C]
    # df_ecos_composite = commonCall(apiKey, '1', '100000', '085Y026', 'MM', '197001', '202201')

    # 소비자동향조사 소비지출전망CSI (~2008년 이전 : 분기, 2008년 이후 ~ : 월)
    # df_ecos_spending_plan = spendingPlan(apiKey, '1', '100000', '085Y026', 'MM', '197001', '202201')

    # 경제성장 (경제성장률, 민간소비증감률 1960년 2분기 ~, 국내 총 투자율 1970년도 1분기 ~ )
    # df_ecos_growth_economic = commonCall(apiKey, '1', '100000', '901Y001', 'QQ', '1960', '2022')


    # 고용지표 (실업률, 고용률 1999년 6월 ~, 제조업 평균가동률 1980년 1월 ~, 제조업 재고율지수 1985년 1월 ~)
    # df_ecos_growth_economic = commonCall(apiKey, '1', '100000', '901Y001', 'MM', '196001', '202201')

    # 물가지수 (소비자/생산자 - 1966년 1월 ~, 근원 인플레이션 - 1991년 1월, 주택매매 - 2004년 11월 ~, 수출/수입 - 1972년 1월 ~)
    # df_ecos_price_index = commonCall(apiKey, '1', '100000', '901Y001', 'MM', '196001', '202201')

    # 통화금융증권 (M1(평잔) 증감률 - 1971년 1월 ~ , M2(평잔) 증감률 - 1987년 1월 ~ , CD(91일) 수익률 - 1991년 3월 ~ , 국고채(3년) 수익률 - 1995년 5월 ~)
    #df_ecos_currency_finance = commonCall(apiKey, '1', '100000', '901Y001', 'MM', '196001', '202201')

    # 국제무역수지 ( 외환보유액 - 1971년 1월 ~, 경상수지, 상품수지, 서비스수지 - 1980년 1월 ~) 기간 MM, YY 두가지
    #df_ecos_balance_of_payment = commonCall(apiKey, '1', '100000', '901Y001', 'YY', '195001', '202201')

    # 국내 총생산 ( GDP - 1953년 ~ )
    df_ecos_gdp = commonCall(apiKey, '1', '100000', '111Y002', 'YY', '1950', '2022')