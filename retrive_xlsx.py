from datetime import datetime
from pytse.pytse import PyTse,SymbolData
import pickle
from tse_constants import FILE_PATH
import xlsxwriter


def get_buy_minus_sell(symbols):
    num = 0
    sum = 0
    for x in symbols:
        symbol = symbols[x]
        sym_name = str(symbol.l18)
        # print(sym_name,symbol)
        if hasattr(symbol,'ct'):
            num = num + 1
            buy_i_vol = symbol.ct.Buy_I_Volume
            sell_i_vol = symbol.ct.Sell_I_Volume
            price_commited = symbol.pc
            temp_sum=(buy_i_vol - sell_i_vol) * price_commited
            sum = sum + temp_sum
            print(sym_name,temp_sum)
    print(f"num={num} , sum={sum}")

def get_sum_val(symbols,date):
    num = 0
    sum = 0
    for x in symbols:
        symbol = symbols[x]
        sym_name = str(symbol.l18)
        num = num + 1
        sum = sum + int(symbol.tval)
        print(sym_name,symbol.tval)
    print(f"num={num} , sum={sum}")

    workbook = xlsxwriter.Workbook('tse_1.xlsx') 
    worksheet = workbook.add_worksheet("tval %") 
    col=0
    row=0
    #col 0 -> name / col 1 -> tval
    worksheet.write(row,col,"name")
    worksheet.write(row,col+1,date)
    row = row + 1
    for x in symbols:
        symbol = symbols[x]
        if int(symbol.tval) != 0:
            sym_name = str(symbol.l18)
            worksheet.write(row,col,sym_name)
            worksheet.write(row,col+1,int(symbol.tval)*100/sum)
            row = row + 1
    workbook.close()

# %Y%m%d like 20201119
# date = "20201119"
date = "20201122"
file_name = f"tse_{date}.pkl"
# file_name = f"tse.pkl"
with open(f"{FILE_PATH}\\{file_name}", 'rb') as input:
    symbols = pickle.load(input)
    # get_buy_minus_sell(symbols)
    get_sum_val(symbols,date)
