import pandas as pd
import matplotlib.pyplot as plt

csv_path = r'F:\guvi\Capstone Projects\STOCK-project\DATA\csv'

def get_df(csv_filename):
    df = pd.read_csv(f"{csv_path}\{csv_filename}")
    return df

def get_df_with_returns(csv_filename):
    df = pd.read_csv(f"{csv_path}\{csv_filename}")
    df["daily_return"] = df["close"].pct_change()
    df['cumulative_return'] = (df['daily_return'].fillna(0).add(1).cumprod())
    return df


    
