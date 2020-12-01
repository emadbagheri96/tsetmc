from datetime import datetime
from pytse.pytse import PyTse,SymbolData
import pickle
from tse_constants import FILE_PATH
import time

def write_to_file(symbols):
    todaydate = datetime.today().strftime('%Y%m%d')
    file_name=f"tse_{todaydate}.pkl"
    with open(f"{FILE_PATH}\\{file_name}", 'wb') as output:
        print(f"{file_name} created")
        pickle.dump(symbols,output,pickle.HIGHEST_PROTOCOL)
    print("Saved!")

print("Start")
pytse=PyTse()#read_symbol_data=True,read_client_type=False
pytse.read_client_type()
symbols=pytse.symbols_data
print("Load Begin")

symbols_id_list = set()
for x in symbols:
    symbols_id_list.add(x)

while len(symbols_id_list)!=0:
    for x in symbols_id_list.copy():
        try:
            symbols[x].fill_data()
        except:
            print("*** ERROR! :",str(symbols[x].l18))
        else:
            print(str(symbols[x].l18))
            symbols_id_list.remove(x)
        # time.sleep(1)
print("Load Finished")
write_to_file(symbols)