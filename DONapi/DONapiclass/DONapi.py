import csv
import json
import math
import os
import re
import urllib.parse
from collections import Counter

import joblib
import requests
import pandas as pd
import yara

from DONapiclass.node_worker import Node_Worker


class DONapi():
    def __init__(self, package:str, from_local:bool=False): 
        absolute_file_path = os.path.abspath(__file__)
        current_working_directory = os.getcwd()
        relative_file_path = os.path.relpath(absolute_file_path,
                                             current_working_directory)
        relative_dir = os.path.dirname(relative_file_path)
        
        self.features = {}
        
        self.top_1_mill = []
        with open('top-1m.csv', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            for row in csvreader:
                self.top_1_mill.append(row[1])
                
        if from_local:
            data = {'package':package}
            URL = 'http://localhost:3000/parsedir'
        else:
            data = {'package': package}
            URL = 'http://localhost:3000/parse'
        
        r = requests.post(URL, json=data)
        if r.status_code == 200:
            from_json = json.loads(r.text)
            self.ast = from_json['ast']
            self.code = from_json['code']
            self.shell = from_json['shell']
        else:
            print(r.text)
            raise Exception(f'Error in fetching data from the server, status code: {r.status_code}, text: {r.text}')

    def Malicious_Shell_Command_Detector(self):
        rules = yara.compile(filepath='rules.yara')
        to_match = self.code+self.shell
        matches = rules.match(data=to_match)
        for i in range(1,9):
            self.features[f'R{i}'] = 0
        for match in matches:
            self.features[match.rule] = len(match.strings)

    def Malicious_Domain_Detector(self):
        def calculate_entropy(string):
            probabilities = [n_x / len(string) for x, n_x in Counter(string).items()]
            entropy = -sum([p * math.log(p) / math.log(2.0) for p in probabilities])
            return entropy
        
        def count_vowels_consonants(string:str)->tuple[int]:
            vowels = "aeiou"
            consonants = "bcdfghjklmnpqrstvwxyz"
            num_vowels = sum(1 for char in string if char in vowels)
            num_consonants = sum(1 for char in string if char in consonants)
            return num_vowels, num_consonants
        
        def Modify_file_permissions_and_create_processes(string:str)->int:
            iteration = 0
            max_iterations = 10
            decoded_string = string

            while '%' in decoded_string and iteration < max_iterations:
                try:
                    decoded_string = urllib.parse.unquote(decoded_string)
                except:
                    break
                iteration += 1
            check_commands = ['chmod','chown','chgrp','/bin/bash','/bin/sh','bin']
            for command in check_commands:
                if command in decoded_string:
                    return 1
            return 0
        
        def percentage(part, whole):
            return 100 * float(part) / float(whole) if whole != 0 else 0
        
        def gibberish_test(string):
            num_vowels, num_consonants = count_vowels_consonants(string)
            total = num_vowels + num_consonants
            bool_gib = percentage(num_vowels, total) < 50
            if bool_gib:
                return 1
            return 0
        ### EOFs
        
        URL_regex = r'\bhttps?:\/\/((?:[a-zA-Z0-9-]+\.)+[a-zA-Z0-9-]+\.[a-zA-Z]{2,})(\/[^\s]*)?\b'
        to_match = self.code+self.shell
        domain_with_longest_subdomain = ''
        longest_subdomain = ''
        permissions_and_create_processes = 0
        for found in re.finditer(URL_regex, to_match):
            domain = found.group(1)
            splited = domain.split('.')
            right_side =  '.'.join(splited[-2:])
            if right_side in self.top_1_mill:
                continue
            if not splited[-1].isalpha():
                continue
            if len(splited) < 3:
                continue
            if permissions_and_create_processes == 0:
                permissions_and_create_processes = Modify_file_permissions_and_create_processes(found.group(0))
            left_side = splited[:-2]
            localmax = max(left_side)
            if len(localmax) > len(longest_subdomain):
                longest_subdomain = localmax
                domain_with_longest_subdomain = found.group(0)
        
        ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        found = re.findall(ip_regex, to_match)
        if found:
            for ip in found:
                if not ip.startswith('192.168') and not ip.startswith('10.'):
                    if not ip.startswith('172.16') and not ip.startswith('100.64'):
                        self.features['UF10'] = 1
        else:
            self.features['UF10'] = 0
            
        
        entropy = calculate_entropy(longest_subdomain)
        longest_subdomain_length = len(longest_subdomain)
        vowels, consonants = count_vowels_consonants(longest_subdomain)
        consecutive = sum(1 for i in range(1, len(longest_subdomain)) if longest_subdomain[i] == longest_subdomain[i-1])
        repeated = len(longest_subdomain) - len(set(longest_subdomain))
        numeric = sum(1 for char in longest_subdomain if char.isdigit())
        gibberish = gibberish_test(longest_subdomain)

        self.features['UF1'] = entropy
        self.features['UF2'] = longest_subdomain_length
        self.features['UF3'] = percentage(vowels, longest_subdomain_length)
        self.features['UF4'] = percentage(consonants, longest_subdomain_length)
        self.features['UF5'] = percentage(consecutive, longest_subdomain_length)
        self.features['UF6'] = percentage(repeated, longest_subdomain_length)
        self.features['UF7'] = percentage(numeric, longest_subdomain_length)
        self.features['UF8'] = permissions_and_create_processes
        self.features['UF9'] = gibberish
    
    def Obfuscated_Code_Detector(self):
        code = self.code.lower()
        before = code
        while '\n\n' in code:
            code = code.replace('\n\n','\n')
        while '  ' in code:
            code = code.replace('  ',' ')
        OF1 = len(code)/len(before)
        OF2 = code.count(' ')/before.count(' ')
        OF3check = ('charAt','indexOf','lastIndexOf','match','toLowerCase','toUpperCase','charCodeAt',
                    'trimStart','trimEnd','padStart','padEnd','fromCharCode','toString','valueOf','toSource','localeCompare',
                    'Array.from')
        OF3check = set(x.lower() for x in OF3check)
        OF3 = 0
        for func in OF3check:
            OF3 += code.count(func)
        OF4check = ('concat','includes','replace','repeat','search','slice','split','substr','substring','trim',
                    'join','reverse','sort','fill','pop','push','shift','unshift','btoa','atob','escape','unescape')
        OF4check = set(x.lower() for x in OF4check)
        OF4 = 0
        for func in OF4check:
            OF4 += code.count(func)
        OF5check = ('+','-','++','--','~','!','*','/','%','<<','>>','>>>','<','>','<=','>=','==','===','!=','!==',
                    '&','^','|','&&','||','?','=','+=','-=','*=','/=','%=','<<=','>>=','>>>=','&=','^=','|=')
        OF5check = set(x.lower() for x in OF5check)
        OF5 = 0
        for func in OF5check:
            OF5 += code.count(func)
        OF6 = len([x for x in code.splitlines() if not x.startswith('//')])
        OF7 = code.count(' ')
        OF8check = ('0x','0b','0o','\\x','\\u','\\U')
        OF8 = 0
        for check in OF8check:
            OF8 += code.count(check)
        OF9regex = r' ([a-zA-Z_0-9]+) ?='
        identifiers = []
        for found in re.finditer(OF9regex, code):
            identifiers.append(found.group(1))
        total = sum(len(s) for s in identifiers)
        OF9 = total/len(identifiers) if identifiers else 0
        all_chars = ''.join(identifiers)
        char_count = Counter(all_chars)
        total_chars = sum(char_count.values())
        char_prob = {char: count/total_chars for char, count in char_count.items()}
        OF10 = -sum(prob * math.log(prob) for prob in char_prob.values())
        OF11 = len(max(code.splitlines(), key=len))
        N = 20
        OF12 = len([x for x in code.splitlines() if len(x) > N])
        OF13regex = r'[a-zA-Z_0-9]+\.[a-zA-Z_0-9]+\(.*?\)'
        OF13 = len(re.findall(OF13regex, code))
        OF14 = code.count('if')
        OF15 = code.count('for')
        OF16 = code.count('while')
        OF17 = code.count('switch')
        OF18 = code.count('case')
        OF19 = code.count('function')
        OF20 = code.count('return')
        OF21 = code.count('try')
        OF22 = code.count('catch')
        OF23 = code.count('throw')
        OF24 = code.count('new')
        OF25 = code.count('delete')
        OF26 = code.count('continue')
        OF27 = code.count('else')
        for i in range(1,28):
            self.features[f'OF{i}'] = locals()[f'OF{i}']
    
    
    def Suspicious_Package_Static_Identifier(self):
        worker = Node_Worker()
        ast = self.ast
        def traverse_dict(node:list|dict, depth=0):
            indent = '  ' * depth
            if isinstance(node, dict):
                for key, value in node.items():
                    if hasattr(worker,'visit_'+key):
                        getattr(worker,'visit_'+key)(value)
                    traverse_dict(value, depth + 1)
            elif isinstance(node, list):
                for index, value in enumerate(node):
                    traverse_dict(value, depth + 1)
        traverse_dict(ast)
        for key, value in worker.SPSI_features.items():
            self.features[key] = value
            
    def model_eval(self):
        df = pd.DataFrame([self.features])
        obfuscated_features = ['OF1','OF2', 'OF3', 'OF4', 'OF5', 'OF6', 'OF7', 'OF8', 'OF9', 'OF10', 'OF11',
            'OF12', 'OF13', 'OF14', 'OF15', 'OF16', 'OF17', 'OF18', 'OF19', 'OF20',
            'OF21', 'OF22', 'OF23', 'OF24', 'OF25', 'OF26', 'OF27']
        behavior_features = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'UF10',
                'UF1', 'UF2', 'UF3', 'UF4', 'UF5', 'UF6', 'UF7', 'UF8', 'UF9',
                'BF1', 'BF2', 'BF3', 'BF4', 'BF5', 'BF6', 'BF7', 'BF8', 'BF9', 'BF10', 'BF11', 'BF12']
        decision_features = ['obfuscated_predict', 'obfuscated_0_proba', 'obfuscated_1_proba',
                            'behavior_predict', 'behavior_0_proba', 'behavior_1_proba']
        
        decision_df = pd.DataFrame()

        obfuscated_model = joblib.load('models/obfuscated_model.pkl')
        behavior_model = joblib.load('models/behavior_model.pkl')
        decision_model = joblib.load('models/decision_model.pkl')
        
        X = df[obfuscated_features]
        
        decision_df['obfuscated_predict'] = obfuscated_model.predict(X)
        decision_df[['obfuscated_0_proba', 'obfuscated_1_proba']] = obfuscated_model.predict_proba(X)
        print('_'*50)
        print(f'Obfuscated Model prediction: {decision_df["obfuscated_predict"].values[0]}')
        print(f'Obfuscated Model 0 class confidence: {decision_df["obfuscated_0_proba"].values[0]}, 1 class confidence: {decision_df["obfuscated_1_proba"].values[0]}')
        
        X = df[behavior_features]
        
        decision_df['behavior_predict'] = behavior_model.predict(X)
        decision_df[['behavior_0_proba', 'behavior_1_proba']] = behavior_model.predict_proba(X)
        print('_'*50)
        print(f'Behavior Model prediction: {decision_df["behavior_predict"].values[0]}')
        print(f'Behavior Model 0 class confidence: {decision_df["behavior_0_proba"].values[0]}, 1 class confidence: {decision_df["behavior_1_proba"].values[0]}')
        
        X = decision_df[decision_features]
        
        model_decision = decision_model.predict(X)
        decision_proba = decision_model.predict_proba(X)
        print('_'*50)
        print(f'Decision Model prediction: {model_decision[0]}')
        print(f'Decision Model 0 class confidence: {decision_proba[0][0]}, 1 class confidence: {decision_proba[0][1]}')
        print('_'*50)
        if model_decision[0]:
            print('The package is malicious!!!')
        else:
            print('The package is benign')
        
    
            
if __name__ == "__main__":
    don = DONapi('tar')
    don.Malicious_Shell_Command_Detector()
    don.Malicious_Domain_Detector()
    don.Obfuscated_Code_Detector()
    don.Suspicious_Package_Static_Identifier()