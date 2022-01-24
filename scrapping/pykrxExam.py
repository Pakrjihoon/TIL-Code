from pykrx import stock
import pandas as pd
import csv

# f = open('business_days.csv', 'r', encoding='utf-8')
# rdr = csv.reader(f)
#
# df = pd.DataFrame(rdr)
# for i in range(0, 5):
# #for i in range(0, len(df)):
#      # print(df.loc[[i], [0]])
#     strPd = (df.loc[[i], [0]])
#     print(strPd)
#
# f.close()
f = open('business_days.csv', 'r')
while True:
    line = f.readline()
    line = line.strip().replace("-", "")
    df = stock.get_market_cap_by_ticker(line)
    # date = [line]
    # df['date'] = date
    print(df)
    # df.to_csv('test1.csv')
    if not line: break
f.close()
# df = stock.get_market_cap_by_ticker("20000101")
#
# df.to_csv('test.csv')
# list = stock.get_previous_business_days(fromdate="19940101", todate="20220117")
# df = pd.DataFrame(list)
# df.to_csv('business_days.csv')
# print(df)
