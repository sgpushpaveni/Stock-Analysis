# Data Driven Stock Analysis

## Project Overview  
1.	Provide a comprehensive visualization and analysis of the Nifty 50 stocks' performance over the past year
2.	Analyze daily stock data, including open, close, high, low, and volume values
3.	Clean and process the data
4.	Generate key performance insights
5.	Visualize the top-performing stocks in terms of price changes, as well as average stock metrics
6.	Offer interactive dashboards using Streamlit and Power BI 
7.	Help Investors, analysts, and enthusiasts make informed decisions based on the stock performance


## Technologies  
- **Programming Language**: Python
- **Database**: MySQL  
- **Visualization Tools**: Streamlit, Power BI 
- **Web Application**: Streamlit
- **Libraries**: PyYaml, Matplotlib, SQLAlchemy, Seaborn  
- **Data Processing**: Pandas, Numpy


## Business Use Cases  
- **Stock Performance**:
-- Top 10 best and worst performing stocks
- **Market Overview**:
  - Provide an overall market summary 
  - Average stock performance 
  - Insights into the percentage of green vs red stocks
  

### Clone the git Repository  
```bash
https://github.com/sgpushpaveni/Stock-Analysis.git
```

### Install Dependencies
Dependencies installed for this project:
- Python 3.13+
- pip install pyyaml, python-csv, pandas streamlit numpy mysql-connector-python
- MySQL workbench


## Run the Streamlit Application
```bash
streamlit run app.py
```

## File Structure
```bash
Stock-project/
├─ CODE/
| ├─ app_common/
| │  ├─ __pycache__/
| │  │  ├─ __init__.cpython-313.pyc
| │  │  ├─ db_operations.cpython-313.pyc
| │  │  └─ df_operations.cpython-313.pyc
| │  ├─ __init__.py
| │  ├─ db_operations.py
| │  └─ df_operations.py
| ├─ app_pages/
| │  └─ app_views.py
| ├─ data_processing/
| │  └─ yml2csv.ipynb
| └─ app.py
└─ readme.md
```

## Dataset
  Stock data coulmns:
  - Ticker
  - Day
  - Month
  - Open
  - close
  - High 
  - Low 
  - Volume

