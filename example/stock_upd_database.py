import data.stock as st
import pandas as pd

code = '000001.XSHE'

# 调用一只股票的行情数据
data = st.get_single_stock_price(code=code,
                           time_freq='daily',
                           start_date='2021-02-01',
                           end_date='2021-03-01')

# 存入csv
st.export_data(data=data, filename=code, type='price')

# 从csv中获取数据
data = st.get_csv_data(code, 'price')
print(data)


# 实时更新数据：假设每天更新日K数据>存到csv文件里面>data.to_csv(append)


