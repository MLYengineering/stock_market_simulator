#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 09:56:56 2021

@author: mathiaslichy
"""

import streamlit as st
import streamlit.components.v1 as components 
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import date
import pandas as pd
import matplotlib
from fbprophet import Prophet


st.title('What if....you invested monthly in Apple for 5 years ?')


def get_df_sum(hist,user_invest,user_start):
    user_invest=int(user_invest)
    df_sum = pd.DataFrame (columns = ['date','invest','kurs','anteile_neu','anteile_gesamt','wert_gesamt','wert_ohne'])
    date_follow=user_start
    i=0
    hist_date_index=hist.copy().set_index('Date')

    while date_follow < hist.loc[len(hist.index)-1,'Date']:
        ##### prüfe ob datum in df vorhanden
        temp_date=date_follow
        while hist[hist['Date']==temp_date].empty == True:
            temp_date=temp_date+ pd.DateOffset(days=1)
    
        df_sum.at[i,'date']=temp_date
        df_sum.at[i,'kurs']=float(hist_date_index.loc[df_sum.loc[i,'date'],'Close'])
        df_sum.at[i,'invest']=user_invest
        df_sum.at[i,'anteile_neu']=user_invest/float(df_sum.loc[i,'kurs'])
        if i==0:
            df_sum.at[i,'anteile_gesamt']=df_sum.loc[i,'anteile_neu']
        else:
            df_sum.at[i,'anteile_gesamt']=df_sum.loc[i,'anteile_neu']+df_sum.loc[i-1,'anteile_gesamt']
        df_sum.at[i,'wert_gesamt']=df_sum.loc[i,'anteile_gesamt']*df_sum.loc[i,'kurs']
        df_sum.at[i,'wert_ohne']=(i+1)*user_invest
        i=i+1
        date_follow=date_follow+ pd.DateOffset(months=1)
    return df_sum
    

def plot_graphs(df):
    df['date']=pd.to_datetime(df['date'])
    df['kurs']=pd.to_numeric(df['kurs'])
    df['wert_gesamt']=pd.to_numeric(df['wert_gesamt'])
    df['wert_ohne']=pd.to_numeric(df['wert_ohne'])
    
    fig = plt.figure(figsize=(10, 3 ))
    # ax1=fig.add_subplot(211)
    
    # sb.lineplot(x=df['date'], y=df['kurs'],  dashes= False, color='#DE3163')
    # plt.xlabel('Date')
    # plt.ylabel('stock')
    
    
    ax2=fig.add_subplot(111)
    
 
    sb.lineplot(x=df['date'], y=df['wert_gesamt'],  dashes= False, label='Amount with stock investments')
    sb.lineplot(x=df['date'], y=df['wert_ohne'],  dashes= False, label='Amount of investments')
    plt.xlabel('Date')
    plt.ylabel('amount')
    ax2.ticklabel_format(style='plain', useOffset=False, axis='y')
    ax2.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    
    st.pyplot(fig)





user_input = st.text_input("Stock symbol, for example for Apple insert AAPL - check out https://de.finance.yahoo.com", 'AAPL')

col1,col2, col3  = st.beta_columns(3)

#user_invest = col1.text_input("monthly amount of investment", '500')
user_invest = col1.slider("monthly amount of invest", 10,2000,500,10)
#user_start= st.text_input("start date", '2005-02-08')

initial_date=pd.to_datetime('2015-01-01')
min_date=initial_date-pd.DateOffset(years=5)
max_date=date.today()-pd.DateOffset(months=5)
user_start= col3.date_input('First day of monthly invest', value=initial_date, min_value=min_date, max_value=max_date, key=None)


user_start=pd.to_datetime(user_start)


msft = yf.Ticker(user_input)
hist = msft.history(start=user_start)

#col2.write('Savings plans and monthly investments in stock prices can produce huge profits in just a few years. Here you can see the effect over time ')


st.subheader('For tired developers, coffee is essential - please send me a virtual coffee for more sites - only 2 USD ')


components.html(
    """
    <form action="https://www.paypal.com/donate" method="post" target="_top">
    <input type="hidden" name="business" value="mathias.lichy@me.com" />
    <input type="hidden" name="currency_code" value="USD" />
    <input type="hidden" name="amount" value="2" />
    <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
    <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
    </form>
    """,
    height=50,
)
    



if hist.empty == True:
    st.markdown('some problem occured: stock not found or date in future - pls. check https://de.finance.yahoo.com for available stocks')

else:
    hist=hist.reset_index()
    hist['Date']=pd.to_datetime(hist['Date'])
    if user_start < hist.loc[0,'Date']:
        user_start=hist.loc[0,'Date']
    df=get_df_sum(hist,user_invest,user_start)
    st.header('Result')

    
    col4,col5, col6  = st.beta_columns(3)
    col4.markdown('Amount of investment')
    
    col5.markdown('Result with investment')
    col6.markdown('DELTA')
    amount_invest=df.loc[len(df.index)-1,'wert_ohne']
    col4.markdown(str(amount_invest)+ ' USD')
    amount_overall=df.loc[len(df.index)-1,'wert_gesamt']
    col5.markdown(str(int(amount_overall))+ ' USD')
    col6.markdown(str(int((amount_overall/amount_invest-1)*100))+ ' %')
    
    
    
    plot_graphs(df)







