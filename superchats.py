from rich import print
from rich.console import Console

import re
import pandas as pd
import numpy as np

import os
from io import StringIO
import datetime

import typer                #user interface library

console = Console()
app = typer.Typer()

@app.command()
def mainloop(filename: str):     #read in file from command line
    pd.set_option('display.max_colwidth', None)   #Show full columns and Rows
    pd.set_option('display.max_rows', None)
    textfile = open(filename, 'r')  
    filetext = textfile.read()   #dump contents of the file into the filetext variable
    textfile.close()             #close the file
    matches = re.findall(r"(.+) ([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]),[\s]([0-9][0-9]:[0-9][0-9])([\s][\S]*)([\s][\S]*)[|▶ ]Go to:([\s][\S]*)\n([Donated:]+) ([$]\d+.\d+)", filetext)
    df = pd.DataFrame(matches)   # df.rename(columns={"A": "a", "B": "c"})
    df[8] = df[1] + ' ' + df[2]  # concatenate Date and Time fields before conversion to Datetime type.
    df[8] = pd.to_datetime(df[8])
    df[7] = df[7].replace({'\$':''}, regex = True) #Remove the '$' from the Superchat amount column
    df[7] = pd.to_numeric(df[7])  # convert Superchats column to the Float datatype to accommodate the decimal value
    del df[1]                     # delete columns 1,2,3,4 and 6.
    del df[2]
    del df[3]
    del df[4]
    del df[6]
    df = df.rename(columns={0:'Youtube_ID',5:'Video_Location_Time',7:'Superchat',8:'Timestamp'})  #name the columns
    console.print("........................INDIVIDUAL SUPERCHATS BY TIMESTAMP.....................................",style="cyan")
    console.print("\n", df.round(2), "\n")
    #print(df['Superchat'].describe())
    console.print("........................BIGMAN7917's STATISTICS.................................................\n", style="cyan")
    if df[(df['Youtube_ID'] == 'BIGMAN7917') & (df['Superchat'] >= 1)].empty:
        console.print("[bold]ZERO[/] donations from [cyan][bold]BIGMAN7917[/][/]", style="bold red")
    else:    
        console.print(df[(df['Youtube_ID'] == 'BIGMAN7917') & (df['Superchat'] >= 1)].round(2), "\n")  # ['Superchat'].sum() for total.
        console.print("BIGMAN7917 TOTAL SUPERCHATS:  " ,df[(df['Youtube_ID'] == 'BIGMAN7917')]['Superchat'].sum().round(2), "\n")
        console.print(df[(df['Youtube_ID'] == 'BIGMAN7917')]['Superchat'].describe().round(2), "\n")   #about Bigman's donations
    #together = [df, df2]
    #df3 = pd.concat(together)
    console.print("SUPERCHATS BY USER_ID\n")
    IDsortedData = df.groupby(['Youtube_ID'])['Superchat'].sum().round(2)
    console.print(IDsortedData, "\n")
    console.print("........................TOP SUPERCHATTERS!........................", "\n", IDsortedData.sort_values(ascending=False).head(), "\n", style="cyan")
   # console.print("TOP SUPERCHATTERS!", "\n", df.groupby(['Youtube_ID'])['Superchat'].sum(), "\n")
    console.print("TOTAL SUPERCHATS:  ", df['Superchat'].sum().round(2), "\n")
    console.print(df['Superchat'].describe())
    #df.to_excel(filename + ".xlsx")
    df.to_xml(filename + ".xml")

if __name__ == "__main__":
    app()
