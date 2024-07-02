import os
import sys

import pandas as pd

from DONapiclass.DONapi import DONapi

CSV_FILE = 'trash.csv'


def csv_input(features:dict,package:str,malicious:int)->None:
    if os.path.exists(CSV_FILE):
        df = pd.DataFrame([features])
        df.insert(0, 'package', package)
        df['malicious'] = malicious
        df['obfuskated'] = 0
        df.to_csv(CSV_FILE, mode='a', header=False, index=False)
    else:
        df = pd.DataFrame([features])
        df.insert(0, 'package', package)
        df['malicious'] = malicious
        df['obfuskated'] = 0
        df.to_csv(CSV_FILE, index=False)

if __name__ == '__main__':
    path = os.path.join('js_ast_builder/malware_samples/npm')
    for file in os.listdir(path):
        print(file)
        try:
            don = DONapi(file, True)
            don.Malicious_Shell_Command_Detector()
            don.Malicious_Domain_Detector()
            don.Obfuscated_Code_Detector()
            don.Suspicious_Package_Static_Identifier()
            csv_input(don.features,file,1)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                sys.exit(0)
            print('Ошибка на стороне сервера')
            
    packages = []
    with open('validpackages', 'r') as file:
        for line in file:
            packages.append(line.strip())
    packages = packages[:100]
    for package in packages:
        print(package)
        try:
            don = DONapi(package, False)
            don.Malicious_Shell_Command_Detector()
            don.Malicious_Domain_Detector()
            don.Obfuscated_Code_Detector()
            don.Suspicious_Package_Static_Identifier()
            csv_input(don.features, package,0)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                sys.exit(0)
            print('Ошибка на стороне сервера')
        