import pandas as pd
import re


def create_times(df, date_column:str):
    df['date'] = pd.to_datetime(df[date_column]).dt.date
    df['time'] = pd.to_datetime(df[date_column]).dt.time
    df['year'] = pd.to_datetime(df[date_column]).dt.year
    df['month'] = pd.to_datetime(df[date_column]).dt.month_name()
    df['day'] =pd.to_datetime(df[date_column]).dt.day
    df['quarter_year'] = 'Q' + pd.to_datetime(df[date_column]).dt.quarter.astype(str) + ' ' + df['year'].astype(str)
    
    return df

    
def promo_price_cleaner(df, prices: str, promos: str):
    df = df.loc[df[prices].str.contains(r'^\d+\.\d+$')==True]

    new_promo = []

    for promo, price in zip(df[promos], df[prices]):
        price = str(price)
        promo = str(promo)

        if "." in price and price.count('.') == 1:
            promo = promo.replace(".", "")
            promo = promo[:price.index(".")] + "." + promo[price.index("."):]
            if round(float(promo)) > round(float(price)):
                promo = promo.replace(".", "")
                promo = promo[:price.index(".")-1] + "." + promo[price.index(".")-1:]

        if price != 'nan' and price.count('.') == 0:
            promo = promo.replace(".", "")
            promo = promo[:len(price)] + "." + promo[len(price):]
            if round(float(promo)) > round(float(price)):
                promo = promo.replace(".", "")
                promo = promo[:len(price)-1] + "." + promo[len(price)-2:]
        new_promo.append(promo)
    
    df['new_promo'] = new_promo
    #df = df.loc[df['new_promo'].str.contains(r'^\d+\.\d+$')==True]
    df['new_promo'] = pd.to_numeric(df['new_promo'], errors='coerce').astype(float)
    df[prices] = pd.to_numeric(df[prices])
    df['new_promo'] = round(df['new_promo'], 2)
    df = df.loc[df[prices] >= df['new_promo']]

    return df


def product_category(df, types:str, desc:str, name:str):
    
    type_categories = {'8696':'accessories', '13855401': 'keyboard', '1387':'mouse', '1230':'accessories', '1364':'computer', '1325':'accessories', '5384':'audio',
                       '1334':'accessories', '13005399': 'accessories', '12995397': 'accessories', '11865403': 'phone_accessories', '13955395' :'accessories', '1216':'accessories',
                       '12355400': 'accessories', '1276' : 'computer_accessories', '11905404':'others', '12635403':'accessories', '12755395':'accessories', '13835403':'computer_accessories',
                       '1296':'computer', '12285400': 'phone_accessories', '1229':'accessories', '11935397':'storage', '12655397':'storage', '1404':'others', '101781405':'others',  '4259':'audio', '14035403':'phone',
                       '12085400':'accessories', '1282':'computer', '12175397':'storage', '1424':'media', '9094':'security', '1405':'computer_accessories',  '57445397':'storage', '14305406':'computer_accessories',
                       '10142':'battery','12645406':'phone_accessories', '10230':'computer_accessories', '12215397':'storage', '11821715':'audio',  '13555403':'phone_accessories', '14365395':'phone_accessories',
                       '5405':'phone_accessories', '5395':'electrical_appliances', '5398':'audio', '21485407':'phone_accessories', '20642062':'storage', '1280':'others', '1433':'storage', '1515':'battery',
                       '5720':'phone_accessories', '1298':'storage', '13615399':'electrical_appliances', '12585395':'computer_accessories',  '1392':'computer_accessories', '1231':'others', '15435404':'computer_accessories',
                       '1375':'computer_accessories', '42945397':'storage', '12141714':'computer', '54025401':'accessories', '12575403':'keyboard', '21535407':'accessories', '1416':'others', '24215399':'watch_accessories',
                       '11434':'computer_accessories', '2434':'watch_accessories', '2449':'watch_accessories',  '2425':'watch_accessories', '13621714':'phone', '24861714':'phone', '24821716':'phone',
                       '54864259':'tv_accessories', '1714':'phone', '51601716':'phone', '51871714':'computer', '5403':'computer_accessories', '54085407':'computer_accessories', '24885185':'watch', '24895185':'watch',
                       '5407':'phone_accessories', '5406':'others', '5404':'others', '85641716':'phone', '42931714':'computer', '24811716':'phone', '85651716':'phone', '2158':'computer', '51882158':'computer',
                       '5401':'keyboard', '12051714':'others', '5399':'phone_accessories', '1716':'phone', '21622158':'computer', '12031714':'computer', '51861714':'computer', '21571716':'phone', '106431714':'phone',
                       '21632158':'computer', '79201715':'audio', '21561716':'phone', '51902158':'computer', '113291716':'phone', '113281716':'phone', '113271716':'phone', '113851714':'computer', '11859':'others',
                       '118692158':'computers', '51912158':'computer', '113464259':'audio', '12282':'watch_accessories'}
                       
    df['product_category'] = df[types].astype(str).map(type_categories).fillna('Unknown')

    df.loc[((df['product_category']=='accessories') & (df[desc].str.contains('imac|pc|macbook|mac', case=False))), 'product_category'] = 'computer_accessories'
    df.loc[((df['product_category']=='accessories') & (df[desc].str.contains('iphone', case=False))), 'product_category'] = 'phone_accessories'
    df.loc[((df['product_category']=='computers') & (df[desc].str.contains('ipad', case=False))), 'product_category'] = 'tablets'
    df.loc[((df['product_category']=='phone') & (df[desc].str.contains('ipad', case=False))), 'product_category'] = 'tablets'
    df.loc[((df['product_category']=='Unknown') & (df[desc].str.contains('laptop|computer|imac|macbook', case=False))), 'product_category'] = 'computers'
    df.loc[((df['product_category']=='Unknown') & (df[desc].str.contains('case', case=False))), 'product_category'] = 'phone_accessories'
    df.loc[((df['product_category']=='Unknown') & (df[desc].str.contains('repair|diagnosis|labor', case=False))), 'product_category'] = 'insurance'
    df.loc[((df['product_category']=='storage') & (df[desc].str.contains('monitor', case=False))), 'product_category'] = 'computers'
    df.loc[((df['product_category']=='storage') & (df[desc].str.contains('laptop', case=False))), 'product_category'] = 'computers'
    df.loc[((df['product_category']=='storage') & (df[desc].str.contains('smartwatch', case=False))), 'product_category'] = 'watch'
    df.loc[((df['product_category']=='storage') & (df[name].str.contains('apple iphone', case=False))), 'product_category'] = 'phone'
    df.loc[((df['product_category']=='storage') & (df[name].str.contains('apple ipad', case=False))), 'product_category'] = 'tablets'
    df.loc[((df['product_category']=='others') & (df[desc].str.contains('smartwatch|Smart Watch', case=False))), 'product_category'] = 'watch'
    df.loc[((df['product_category']=='others') & (df[name].str.contains('power wireless sensor', case=False))), 'product_category'] = 'electrical_accessories'
    df.loc[((df['product_category']=='others') & (df[name].str.contains('motion sensor', case=False))), 'product_category'] = 'security'
    df.loc[((df['product_category']=='others') & (df[desc].str.contains('baby monitor', case=False))), 'product_category'] = 'security'
    df.loc[((df['product_category']=='others') & (df[desc].str.contains('baby monitor', case=False))), 'product_category'] = 'security'
    df.loc[((df['product_category']=='others') & (df[desc].str.contains('selfie', case=False))), 'product_category'] = 'phone_accessories'
    df.loc[((df['product_category']=='others') & (df[name].str.contains('smartwatch', case=False))), 'product_category'] = 'watch'
    df.loc[((df['product_category']=='others') & (df[desc].str.contains('warranty', case=False))), 'product_category'] = 'insurance'
    df.loc[((df['product_category']=='others') & (df[name].str.contains('apple ipad', case=False))), 'product_category'] = 'tablets'

    df.loc[df['product_category'] == 'keyboard', 'product_category'] = 'computer_accessories'
    df.loc[df['product_category'] == 'mouse', 'product_category'] = 'computer_accessories'
    df.loc[df['product_category'] == 'audio', 'product_category'] = 'multimedia'
    df.loc[df['product_category'] == 'media', 'product_category'] = 'multimedia'
    df.loc[df['product_category'] == 'tv_accessories', 'product_category'] = 'multimedia'
    df.loc[df['product_category'] == 'electrical_appliances', 'product_category'] = 'electrical_accessories'
    df.loc[df['product_category'] == 'battery', 'product_category'] = 'electrical_accessories'

    df.loc[(df['product_category'].str.contains('accessories', case=False)), 'product_category'] = 'accessories'
    df.loc[(df['product_category'].str.contains('insurance', case=False)), 'product_category'] = 'services'
    df.loc[(df['product_category'].str.contains('multimedia', case=False)), 'product_category'] = 'media'
    df.loc[(df['product_category'].str.contains('phone', case=False)), 'product_category'] = 'phones'
    df.loc[(df['product_category'].str.contains('unknown', case=False)), 'product_category'] = 'accessories'
    df.loc[(df['product_category'].str.contains('watch', case=False)), 'product_category'] = 'watches'


    return df



def convert_price(record):
    
    if re.match(r'^\d+\.\d{1,3}$', record):
        return record

    else:
        parts = record.split('.')
        if len(parts) == 3:
            return float(record.split('.')[0] + record.split('.')[1] + '.' + record.split('.')[2])
        else:
            return record


def common_orders(record1, record2, key1:str, key2:str):
    
    return record1.merge(record2, how = 'inner', left_on =key1, right_on = key2)
        
















