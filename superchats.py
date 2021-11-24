from rich import print
from rich.console import Console
import re
import pandas as pd
import numpy as np
import typer
import os
from io import StringIO
import datetime

pd.set_option('display.max_colwidth', None)   #Show full columns and Rows
pd.set_option('display.max_rows', None)

console = Console()

app = typer.Typer()

@app.command()
def mainloop(filename: str):
    textfile = open(filename, 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall(r"(.+) ([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]),[\s]([0-9][0-9]:[0-9][0-9])([\s][\S]*)([\s][\S]*)[|▶ ]Go to:([\s][\S]*)\n([Donated:]+) ([$]\d+.\d+)", filetext)
    df = pd.DataFrame(matches)   # df.rename(columns={"A": "a", "B": "c"})
    df[8] = df[1] + ' ' + df[2] # concatenate Date and Time fields before conversion to Datetime type.
    df[8] = pd.to_datetime(df[8])
    #df[5] = df[1] + ' ' + df[5] # concatenate Date and Time fields before conversion to Datetime type.
    #print(df.info())

    df[7] = df[7].replace({'\$':''}, regex = True)   #**Remove the '$'
    # convert Superchats column to Float datatype
    df[7] = pd.to_numeric(df[7])
    del df[1]
    del df[2]
    del df[3]
    del df[4]
    del df[6]
    df = df.rename(columns={0:'Youtube_ID',5:'Video_Location_Time',7:'Superchat',8:'Timestamp'})

    #https://www.geeksforgeeks.org/convert-the-column-type-from-string-to-datetime-format-in-pandas-dataframe/
    print("........................INDIVIDUAL SUPERCHATS BY TIMESTAMP.....................................")
    console.print("\n", df.round(2), "\n")
    #print(df['Superchat'].describe())
    
    print("........................BIGMAN7917's STATISTICS.................................................\n")
    if df[(df['Youtube_ID'] == 'BIGMAN7917') & (df['Superchat'] >= 1)].empty:
        print("..........................")
        console.print("[bold]ZERO[/] donations from [cyan][bold]BIGMAN7917[/][/]", style="bold red")
    
        print("..............................\n")
    else:    
        print(df[(df['Youtube_ID'] == 'BIGMAN7917') & (df['Superchat'] >= 1)].round(2), "\n")  # ['Superchat'].sum() for total.
        print(df[(df['Youtube_ID'] == 'BIGMAN7917')]['Superchat'].describe().round(2), "\n")   #about Bigman's donations
    #together = [df, df2]
    #df3 = pd.concat(together)
    print("SUPERCHATS BY USER_ID\n")
    print(df.groupby(['Youtube_ID'])['Superchat'].sum().round(2), "\n")
    print("TOTAL SUPERCHATS:  ", df['Superchat'].sum().round(2), "\n")
    df.to_excel(filename + ".xlsx")
    df.to_xml(filename + ".xml")

if __name__ == "__main__":
    app()