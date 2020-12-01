from datetime import datetime
from pytse.pytse import PyTse,SymbolData
import pickle
from tse_constants import FILE_PATH
import pandas as pd

# bvol 	حجم مبنا
def get_vol_on_based_vol(data_frame,symbols,date):
    for x in symbols:
        symbol = symbols[x]
        if symbol.tvol != 0 and int(symbol.bvol)!=0:
            sym_name = str(symbol.l18)
            data_frame.at[sym_name,date] = int(symbol.tvol) / int(symbol.bvol)
    return data_frame

#QTotTran5JAvg 	میانگین حجم ماه
def get_vol_on_month_avg_vol(data_frame,symbols,date):
    for x in symbols:
        symbol = symbols[x]
        if hasattr(symbol,'QTotTran5JAvg') and symbol.tvol != 0 and int(symbol.QTotTran5JAvg)!=0:
            sym_name = str(symbol.l18)
            data_frame.at[sym_name,date] = int(symbol.tvol) / int(symbol.QTotTran5JAvg)
    return data_frame

# Tval * Price / BuyerCount
def get_buyer_capitaion(data_frame,symbols,date):
    for x in symbols:
        symbol = symbols[x]
        if hasattr(symbol,'ct') and symbol.tval!=0:
            sym_name = str(symbol.l18)
            if symbol.ct.Buy_CountI!=0 and symbol.ct.Buy_I_Volume!=0:
                data_frame.at[sym_name,date] = symbol.ct.Buy_I_Volume * symbol.pc / symbol.ct.Buy_CountI

    return data_frame

# (BuyVol - SellVol) * closedPrice
def get_buy_minus_sell(data_frame,symbols,date):
    sum = 0
    for x in symbols:
        symbol = symbols[x]
        if hasattr(symbol,'ct'):
            sym_name = str(symbol.l18)
            temp_sum=(symbol.ct.Buy_I_Volume - symbol.ct.Sell_I_Volume) * symbol.pc
            if temp_sum!=0:
                sum = sum + temp_sum
                data_frame.at[sym_name,date]=temp_sum
            # print(sym_name,temp_sum)

    data_frame.at['SUM',date]=sum
    return data_frame

# Tval / Sum
def get_sum_val(data_frame,symbols,date):
    sum = 0
    if not (date in data_frame.columns):
        data_frame[date]=""
        # print(data_frame) # Works
        for x in symbols:
            symbol = symbols[x]
            sum = sum + int(symbol.tval)

        for x in symbols:
            symbol = symbols[x]
            if int(symbol.tval) != 0:
                sym_name = str(symbol.l18)
                data_frame.at[sym_name,date]=int(symbol.tval)/sum*100

        data_frame.at['SUM',date]=sum

    return data_frame

# SellCount / BuyCount
def get_buyer_to_seller_ratio(data_frame,symbols,date):
    if not (date in data_frame.columns):
        data_frame[date]=""
        for x in symbols:
            symbol = symbols[x]
            if hasattr(symbol,'ct'):                  
                sym_name = str(symbol.l18)
                #if symbol.ct.Buy_CountI == 0:
                #     if symbol.ct.Sell_CountI == 0:
                #         data_frame.at[sym_name,date]='NaN'
                #     else:
                #         data_frame.at[sym_name,date]='∞'
                # else:
                    # data_frame.at[sym_name,date]=symbol.ct.Sell_CountI/symbol.ct.Buy_CountI
                if symbol.ct.Buy_CountI != 0:
                    data_frame.at[sym_name,date]=symbol.ct.Sell_CountI/symbol.ct.Buy_CountI

    return data_frame
    
# %Y%m%d like 20201119
# date = "20201122"
dates = ["20201119","20201121","20201122","20201123","20201124","20201125","20201128","20201129","20201130","20201201"]
pd_tval = pd.DataFrame()
pd_buyer_seller_ratio = pd.DataFrame()
pd_buyer_minus_seller = pd.DataFrame()
pd_buyer_capitaion = pd.DataFrame()
pd_based_vol = pd.DataFrame()
pd_month_avg_vol = pd.DataFrame()

for date in dates:
    file_name = f"tse_{date}.pkl"
    with open(f"{FILE_PATH}\\{file_name}", 'rb') as input:
        symbols = pickle.load(input)
        # get_buy_minus_sell(symbols)
        pd_tval = get_sum_val(pd_tval,symbols,date)
        pd_buyer_seller_ratio = get_buyer_to_seller_ratio(pd_buyer_seller_ratio,symbols,date)
        pd_buyer_minus_seller = get_buy_minus_sell(pd_buyer_minus_seller,symbols,date)
        pd_buyer_capitaion = get_buyer_capitaion(pd_buyer_capitaion,symbols,date)
        pd_based_vol = get_vol_on_based_vol(pd_based_vol,symbols,date)
        pd_month_avg_vol = get_vol_on_month_avg_vol(pd_month_avg_vol,symbols,date)


# pd_tval = pd_tval.sort_values(by=dates[-1],ascending=False)
# pd_buyer_seller_ratio = pd_buyer_seller_ratio.sort_values(by=dates[-1],ascending=False)
pd_buyer_minus_seller = pd_buyer_minus_seller.sort_values(by=dates[-1],ascending=False)
pd_buyer_capitaion = pd_buyer_capitaion.sort_values(by=dates[-1],ascending=False)
pd_based_vol = pd_based_vol.sort_values(by=dates[-1],ascending=False)
pd_month_avg_vol = pd_month_avg_vol.sort_values(by=dates[-1],ascending=False)

# pd_buyer_minus_seller.row

print(pd_tval)
print(pd_buyer_seller_ratio)
print(pd_buyer_minus_seller)
print(pd_buyer_capitaion)

with pd.ExcelWriter('tse_panda.xlsx') as writer:
    pd_tval.to_excel(writer,sheet_name="tval %")
    pd_buyer_seller_ratio.to_excel(writer,sheet_name="buyer seller ratio")
    pd_buyer_minus_seller.to_excel(writer,sheet_name="buyer minus seller")
    pd_buyer_capitaion.to_excel(writer,sheet_name="buyer capitation")
    pd_month_avg_vol.to_excel(writer,sheet_name="vol on month avg")
    pd_based_vol.to_excel(writer,sheet_name="vol on based vol")