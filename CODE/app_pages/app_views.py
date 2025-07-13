import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import seaborn as sns
import plotly.express as px
import app_common.df_operations as df_ops

def get_view(view_name, df):
    if view_name == 'Volatility Analysis':
        get_volatility_view(df)
    if view_name == 'Cumulative Return Over Time':
        get_cumulative_view(df)
    if view_name == 'Sector-wise Performance':
        get_sector_view(df)
    if view_name == 'Stock Price Correlation':
        get_corr_view(df)
    if view_name == 'Top 5 Gainers and Losers':
        get_top_gainer_losser(df)

def pre_calculations(df):
    df['date'] = pd.to_datetime(df['date']).dt.date

    df["daily_return"] = df["close"].pct_change()
    # manually calcualte the daily return
    #df["daily_return"] = cal_pct_change(df["close"])
    
    df.dropna(axis=0, inplace=True)
    df.index = df.date
    return df

def get_volatility_view(df):
    st.title('Volatility Analysis')
    st.write("""
        * The Volatility gives insight into how much the price fluctuates, which is valuable for risk assessment. 
        * Higher volatility often indicates more risk, while lower volatility indicates a more stable stock.
        
        """)
    df = pd.DataFrame(df)
    # df['date'] = pd.to_datetime(df['date']).dt.date

    # df["daily_return"] = df["close"].pct_change()
    # # manually calcualte the daily return
    # #df["daily_return"] = cal_pct_change(df["close"])
    
    # df.dropna(axis=0, inplace=True)
    # df.index = df.date
    df_daily_return= df.groupby('Ticker')[['daily_return']]

    volatility = df_daily_return.std().rename(columns={'daily_return':'Volatility'})
    top_volatility = volatility.nlargest(10, ['Volatility'])
    
    bar_plot = px.bar(top_volatility,x=top_volatility.index, y='Volatility',hover_data='Volatility',title='Top 10 Volatility Stocks')
    st.plotly_chart(bar_plot)

    st.dataframe(top_volatility, width=200)
    volatility.to_csv(f"{df_ops.csv_path}/volatility.csv")

def get_volatility_view_OLDDDDDD(df):
    st.title('Volatility Analysis')
    
    df = pd.DataFrame(df)
    df.index = df['date']
    #st.dataframe( df)

    start_dt = df['date'][0]
    end_dt = df.iloc[-1]['date']
    st.write(start_dt)
    st.write(end_dt)
    # df.set_index(pd.date_range(start=start_dt, end=end_dt), inplace=True)

    #df['daily_return'] = df['close'].pct_change()
    df.dropna(axis=0, inplace=True)

    # Calculate standard deviation of daily returns (volatility)
    volatility = df['daily_return'].std()
    st.write(volatility)
    st.dataframe( df)

    # Get the top 10 most volatile stocks
    top_volatility = volatility.nlargest(10)
    st.write(top_volatility)

    bar_plot = px.bar(top_volatility,x='Ticker', y='Volatility',hover_data='Volatility',title='Top Volatility')
    st.plotly_chart(bar_plot)

    # Plotting
    plt.figure(figsize=(10, 6))
    top_volatility.plot(kind='bar', color='skyblue')
    plt.title('Top 10 Most Volatile Stocks Over the Past Year')
    plt.xlabel('Stock Ticker')
    plt.ylabel('Volatility (Standard Deviation of Daily Returns)')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

def cal_pct_change(prices):
    # Initialize an empty list to store the percentage changes
    pct_change = []

    # Shift the prices list by one position to align current and previous prices
    prices_shifted = prices[1:]  # This contains all prices except the first one
    previous_prices = prices[:-1]  # This contains all prices except the last one

    # Calculate percentage change for each period
    for i in range(len(prices_shifted)):
        pct_change.append(prices_shifted[i] / previous_prices[i] - 1)

    return pct_change

def get_cumulative_view(df):
    st.title('Cumulative returns')
    st.write("""
             * An important metric to visualize overall performance and growth over time. 
             * Helps the users compare how the different stocks performs relative to each other.

             """)
    
    df = pd.DataFrame(df)
    df['cumulative_return']= (1 + df["daily_return"]).cumprod() - 1
    finalday_df = df[df['date']==df.iloc[-1]['date']]
    top_tickers = finalday_df.sort_values('cumulative_return', ascending=False)[:5]
    top_df = df[df['Ticker'].isin(list(top_tickers['Ticker']))]
    cumulative_returns= top_df.groupby('Ticker')[['cumulative_return']]

    for stock in cumulative_returns:
        ticker = stock[0]
        ticker_df = pd.DataFrame(stock[1])
        line_plot = px.line(ticker_df,x=ticker_df.index, y='cumulative_return',hover_data='cumulative_return',title=f'Cumulative return of Stock - {ticker}')
        st.plotly_chart(line_plot)

    
def get_sector_view(df):
    st.title('Sector-wise Performance')
    st.write("""
            * Provides a breakdown of stock performance by sector
            * Investors and analysts often look at sector performance to gauge market sentiment in specific industries 
            * The below bar chart represents sectors and its height indicates the average yearly return for stocks within that sector
             """)
    
    sector_data = pd.read_csv(r'F:\guvi\Capstone Projects\STOCK-project\DATA\Sector_data.csv') 
    merged_data = pd.merge(df, sector_data, on='Ticker', how='left')
    # Calculate yearly returns
    merged_data['Year'] = pd.to_datetime(merged_data['date']).dt.year
    years_list = list(merged_data['Year'].unique())
    years_list.insert(0,'Select year')
    year_text = ''
    selected_year = st.selectbox(label="Select an year", options=years_list)

    #st.write(selected_year)
    if selected_year != 'Select year':
        merged_data = merged_data[merged_data['Year']==selected_year]
        year_text = f'for the year - {selected_year}'
        #st.dataframe(merged_data)

    yearly_returns = merged_data.groupby(['Year', 'sector'])['daily_return'].mean().reset_index().rename(columns={'daily_return':'Returns', 'sector':'Sector'})
    average_sector_return = yearly_returns.groupby('Sector')['Returns'].mean().reset_index()
    
    title_text = f'Sector-wise Stocks yearly returns {year_text}'
    bar_plot = px.bar(average_sector_return,x=average_sector_return['Sector'], y=average_sector_return['Returns'],hover_data='Returns', title=title_text)
    st.plotly_chart(bar_plot)

    st.write(f"Sector-wise Yearly returns {year_text}")
    st.dataframe(average_sector_return, width=300)
    st.write('')

def get_corr_view(df):
    st.title('Stock Price Correlation')
    st.write("""
            * The correlation matrix identifies how the stocks are related to each other.
            * The Correlation Heatmap shows the correlation between the closing prices of various stocks. 
            * Darker colors represent higher correlations

             """)

    price_df = df.get(['Ticker','close'])
    #print(price_df.head)
    price_df.reset_index(drop=True, inplace=True)
    #print(price_df.head)
    grouped = (price_df.groupby('Ticker',as_index=False)['close'])

    output_df = pd.DataFrame()
    for stock in grouped:
        output_df[stock[0]] = stock[1].to_list()

    correlation_matrix = output_df.corr()

    map = px.density_heatmap(correlation_matrix,  text_auto=True)
    st.plotly_chart(map)

    st.header('Correlation Matrix')
    st.dataframe(correlation_matrix)

    st.header('Correlation data',)
    st.dataframe(output_df)

def get_top_gainer_losser(df):
    st.title("Top 5 Gainers and Losers (Month-wise)")
    st.write("""
        * Used to observe more granular trends and understand which stocks are gaining or losing momentum on a monthly basis
        * A dashboard-style visualization with charts showing top gainers and losers for each month (12 months total).
    """)
    df = df[df['month']!='2023-10']
    df = df.fillna(0).bfill().ffill()

    df.index = df.date
    price_df = df.get(['Ticker','close', 'date'])
    price_df.reset_index(drop=True, inplace=True)
    grouped = price_df.groupby('Ticker',as_index=False)
    #st.dataframe(grouped)

    data_df = pd.DataFrame()
    for stock in grouped:
        data_df[stock[0]] = stock[1]['close'].to_list()
        data_df.set_index(pd.to_datetime(stock[1]['date']).dt.date,inplace=True )

    data_df.index = pd.to_datetime(data_df.index)
    monthly_returns = data_df.resample('ME').ffill().pct_change().dropna()
    monthly_movers = []

    for month_start_date in monthly_returns.index:
        current_month_data = monthly_returns.loc[month_start_date].sort_values(ascending=False)

        # Get top 5 gainers
        top_5_gainers = current_month_data.head(5).reset_index()
        top_5_gainers.columns = ['Symbol', 'Return']
        top_5_gainers['Type'] = 'Gainer'
        top_5_gainers['Month'] = month_start_date.strftime('%Y-%m')

        # Get top 5 losers
        top_5_losers = current_month_data.tail(5).reset_index()
        top_5_losers.columns = ['Symbol', 'Return']
        top_5_losers['Type'] = 'Loser'
        top_5_losers['Month'] = month_start_date.strftime('%Y-%m')

        monthly_movers.append(top_5_gainers)
        monthly_movers.append(top_5_losers)

    all_monthly_movers = pd.concat(monthly_movers)

    # Create the dashboard-style visualization
    fig, axes = plt.subplots(
        nrows=int(np.ceil(len(all_monthly_movers['Month'].unique()) / 2)),
        ncols=2,
        figsize=(20, 24)
    )  
    # Flatten the axes array for easier iteration
    axes = axes.flatten() 

    for i, month in enumerate(all_monthly_movers['Month'].unique()):
        month_data = all_monthly_movers[all_monthly_movers['Month'] == month]

        # Sort data by return to ensure proper visualization of gainers/losers
        month_data_sorted = month_data.sort_values(
            by='Return', ascending=True if month_data['Type'].iloc[0] == 'Loser' else False
        )

        sns.barplot(
            x='Symbol', y='Return', hue='Type', data=month_data_sorted,
            palette={'Gainer': 'green', 'Loser': 'red'}, ax=axes[i]
        )

        axes[i].set_title(f'Top 5 Gainers and Losers - {month}')
        axes[i].set_xlabel('Stock Symbol')
        axes[i].set_ylabel('Monthly Return (%)')
        axes[i].axhline(0, color='black', linestyle='--', linewidth=0.8)  # Baseline at 0%
        axes[i].tick_params(axis='x', labelrotation	=45) 

    plt.suptitle('Monthly Top 5 Gainers and Losers', fontsize=20, y=1.02) 
    plt.tight_layout(rect=[0, 0, 1, 1])  # Adjust layout to prevent title overlap

    st.pyplot(fig)

    st.header("Stocks Monthly Returns")
    st.dataframe(monthly_returns.sort_index(ascending=True))


def dashboard(df):
    st.title('Dashboard with different dataframes')

    #############################
    st.header("Top 10 Green Stocks")
    df = df.fillna(0).bfill().ffill()

    df.index = df.date
    price_df = df.get(['Ticker','close', 'date'])
    price_df.reset_index(drop=True, inplace=True)
    grouped = price_df.groupby('Ticker',as_index=False)
    st.dataframe(grouped)

    data_df = pd.DataFrame()
    for stock in grouped:
        data_df[stock[0]] = stock[1]['close'].to_list()
        data_df.set_index(pd.to_datetime(stock[1]['date']).dt.date,inplace=True )

    data_df.index = pd.to_datetime(data_df.index)
    yearly_returns = data_df.resample('Y').ffill().pct_change().dropna()
    top_stocks = yearly_returns.transpose()
    top_stocks.reset_index(inplace=True)
    top_stocks.columns = ['Ticker','Returns']
    top_stocks.sort_values(by="Returns")
    #st.dataframe(yearly_returns.head(10))
    st.dataframe(top_stocks, width=300)

    #############################
    st.header("Top 10 Loss Stocks")



    #############################
    st.header("Market Summary")

def powerbi_data_prep(df):
    st.title("PowerBI Data Prep")
    st.write("Data for Power BI dashboard preparation starts.....")
    st.write("")
    datafile_path = r"F:\guvi\Capstone Projects\STOCK-project\DATA\PowerBI"
    df = pd.DataFrame(df)
    # ################################# full data
    df.to_csv(f"{datafile_path}/stocks.csv")

    # ################################ yearly returns
    df = df.fillna(0).bfill().ffill()

    df.index = df.date
    price_df = df.get(['Ticker','close', 'date'])
    price_df.reset_index(drop=True, inplace=True)
    grouped = price_df.groupby('Ticker',as_index=False)
    #st.dataframe(grouped)

    data_df = pd.DataFrame()
    for stock in grouped:
        data_df[stock[0]] = stock[1]['close'].to_list()
        data_df.set_index(pd.to_datetime(stock[1]['date']).dt.date,inplace=True )

    data_df.index = pd.to_datetime(data_df.index)
    yearly_returns = data_df.resample('Y').ffill().pct_change().dropna()
    top_stocks = yearly_returns.transpose()
    top_stocks.reset_index(inplace=True)
    top_stocks.columns = ['Ticker','Returns']
    top_stocks.sort_values(by="Returns")
    top_stocks.to_csv(f"{datafile_path}/yearly_returns.csv")

   # ################################ Monthly returns


    st.write("Data for Power BI dashboard is successully prepared")
