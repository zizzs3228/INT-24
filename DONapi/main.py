import argparse

from DONapiclass.DONapi import DONapi

parser = argparse.ArgumentParser(
                    prog='DONapi',
                    description='Проверка npm пакета на малварность')
parser.add_argument('-p','--package', type=str, required=True, help='Название npm пакета')




if __name__ == '__main__':
    args = parser.parse_args()
    package_name = args.package
    don = DONapi(package_name)
    don.Malicious_Shell_Command_Detector()
    don.Malicious_Domain_Detector()
    don.Obfuscated_Code_Detector()
    don.Suspicious_Package_Static_Identifier()
    don.model_eval()