from datetime import datetime
from pytse.pytse import PyTse,SymbolData
import pickle
from tse_constants import FILE_PATH
import time

print("Start")
pytse=PyTse()#read_symbol_data=True,read_client_type=False
pytse.read_client_type() # در صورت نیاز به اطلاعات حقیقی
symbols=pytse.symbols_data
print("Load Begin")
for x in symbols:
    symbols[x].fill_data()
    print(str(symbols[x].l18))
    # str(symbol.l18)
    time.sleep(1)
print("Load Finished")
todaydate = datetime.today().strftime('%Y%m%d')
file_name=f"tse_{todaydate}.pkl"
with open(f"{FILE_PATH}\\{file_name}", 'wb') as output:
    print(f"{file_name} created")
    pickle.dump(symbols,output,pickle.HIGHEST_PROTOCOL)
print("Saved!")

# ERROR:
# وصنعت