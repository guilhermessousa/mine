import pandas as pd
import os
import glob
from datetime import datetime   
  
input_folder = '/home/diego/Downloads/vli/'
output_folder = '/home/diego/projects/validacao_alerta/tmp/'  

date = datetime.now()
states = {"AC": False, "AL": False, "AP": False, "AM": False, "BA": False, "CE": False, "DF": False, "ES": False, "GO": False, "MA": False, "MS": False, "MT": False, "MG": False, "PA": False, "PB": False, "PR": False, "PE": False, "PI": False, "RJ": False, "RN": False, "RS": False, "RO": False, "RR": False, "SC": False, "SP": False, "SE": False, "TO": False }
  
for f in glob.glob(os.path.join(input_folder, "*.csv")):
    df = pd.read_csv(f, sep=';')
    for index, row in df.iterrows():
        try:
            if row['codEstacao'] in states:
                df.to_csv(f"{output_folder}{date.year}_{row['codEstacao']}_{date.month}.csv", encoding='utf-8', sep=';')
                states[row['codEstacao']] = True
                print(f" - Arquivo do estado {row['codEstacao']} copiado")
                break
            else:
                print(f">>>>>>>>>>>>>>>>>>>Arquivo {f} não está padrão<<<<<<<<<<<<<<<<<<<<<<")
                exit()
        except Exception as err:
            print(err)  
            exit()
            
    
for acronym in states:
    if not states[acronym]:
        print(f">>>>>>>>>>>>>>>>>Arquivo para o estado {acronym} não encontrado<<<<<<<<<<<<<<<")