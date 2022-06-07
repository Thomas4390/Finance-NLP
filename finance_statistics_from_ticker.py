#!/usr/local/bin/python3
import pandas as pd

df = pd.read_csv("sp500.csv")

print(df.head(10))