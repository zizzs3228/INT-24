

class Node_Worker():
    def __init__(self) -> None:
        self.dymanic_source_code_exec = False
        self.dymanic_shell_exec = False
        self.download = False
        self.write_file = False
        self.read_file = False
        self.shells_to_check = ('bash', 'chmod', 'chown', 'chgrp', 'bin', '777','755','/bin/sh')
        self.system_commands_to_check = ('wget','curl','nc','ssh','scp','cat','echo','chmod','iptables','pkill','ps aux')
        self.SPSI_features = {}
        for i in range(1, 12):
            self.SPSI_features[f'BF{i}'] = 0
        self.SPSI_features['BF12'] = 0
    
    def visit_init(self, node:dict|list[dict]):
        if isinstance(node, dict):
            if node.get('type') == 'UnaryExpression':
                if node.get('operator') == '!':
                    if node.get('argument').get('type') == 'BooleanLiteral':
                        if node.get('argument').get('value') == True:
                            return {'type':'BooleanLiteral','value':False}
                        else:
                            return {'type':'BooleanLiteral','value':True}
                elif node.get('operator') == '-':
                    if node.get('argument').get('type') == 'NumericLiteral':
                        return {'type':'NumericLiteral','value':-node.get('argument').get('value')}
            elif node.get('type') == 'MemberExpression':
                if node.get('object').get('type') == 'Identifier' and node.get('property').get('type') == 'Identifier':
                    if node.get('object').get('name') == 'process' and node.get('property').get('name') == 'env':
                        self.SPSI_features['BF2'] = 1
            elif node.get('type') == 'CallExpression':
                if isinstance(node.get('callee'), dict):
                    if node.get('callee').get('name') == 'eval':
                        self.eval_check()
                    elif node.get('callee').get('name') in ('exec', 'execSync','spawn','spawnSync','execFile'):
                        self.exec_check()
                        self.check_shell_commands(node)
                    elif node.get('callee').get('name') in ('writeFile','writeFileSync'):
                        self.write_file_check()
                    elif node.get('callee').get('name') in ('readFile','readFileSync', 'createReadStream'):
                        self.read_file_check()
                    elif node.get('callee').get('name') in ('hostname','platform','arch','type','release'):
                        self.SPSI_features['BF9'] = 1
        return node
    
    def visit_expression(self, node:dict|list[dict]):
        if isinstance(node, dict):
            if node.get('type') == 'CallExpression' and isinstance(node.get('callee'), dict):
                if isinstance(node.get('callee').get('property'), dict):
                    if node.get('callee').get('property').get('name') == 'connect':
                        self.download_upload_check()
                    elif node.get('callee').get('property').get('name') == 'open':
                        if node.get('arguments'):
                            if isinstance(node.get('arguments')[0], dict) and node.get('arguments')[0].get('value') in ('GET','POST','PUT','DELETE','PATCH'):
                                self.download_upload_check()
                    elif node.get('callee').get('property').get('name') in ('get','post','put','delete','patch'):
                        self.download_upload_check()
                    elif node.get('callee').get('property').get('name') in ('exec', 'execSync','spawn','spawnSync','execFile'):
                        self.exec_check()
                        self.check_shell_commands(node)
                    elif node.get('callee').get('property').get('name') in ('writeFile','writeFileSync'):
                        self.write_file_check()
                    elif node.get('callee').get('property').get('name') in ('readFile','readFileSync', 'createReadStream'):
                        self.read_file_check()
                    elif node.get('callee').get('property').get('name') == 'eval':
                        self.eval_check()
                    elif node.get('callee').get('property').get('name') in ('hostname','platform','arch','type','release'):
                        self.SPSI_features['BF9'] = 1
                else:
                    if node.get('callee').get('name') == 'eval':
                        self.eval_check()
                    elif node.get('callee').get('name') in ('exec', 'execSync','spawn','spawnSync','execFile'):
                        self.exec_check()
                        self.check_shell_commands(node)
                    elif node.get('callee').get('name') in ('writeFile','writeFileSync'):
                        self.write_file_check()
                    elif node.get('callee').get('name') in ('readFile','readFileSync', 'createReadStream'):
                        self.read_file_check()
                    elif node.get('callee') in ('hostname','platform','arch','type','release'):
                        self.SPSI_features['BF9'] = 1
                
    
    def visit_callee(self, node:dict|list):
        if isinstance(node, dict):
            if node.get('name') == 'fetch':
                self.download_upload_check()
            elif node.get('name') == 'eval':
                self.eval_check()
            elif node.get('name') in ('exec', 'execSync','spawn','spawnSync','execFile'):
                self.exec_check()
            elif node.get('name') in ('writeFile','writeFileSync'):
                self.write_file_check()
            elif node.get('name') in ('readFile','readFileSync', 'createReadStream'):
                self.read_file_check()
            elif node.get('name') in ('hostname','platform','arch','type','release'):
                self.SPSI_features['BF9'] = 1
            
    def visit_arguments(self, node:dict|list[dict]):
        if isinstance(node, list) and len(node) > 0:
            if node[0] and isinstance(node[0].get('object'), dict) and isinstance(node[0].get('property'), dict):
                if node[0].get('object').get('name') == 'process' and node[0].get('property').get('name') == 'env':
                    self.SPSI_features['BF2'] = 1
                    
    
    
    
    
    ### Help Functitons
    def read_file_check(self)->None:
        self.read_file = True
        if self.download:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF1'] = 1
        if self.dymanic_shell_exec:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF5'] = 1
        if self.dymanic_source_code_exec:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF6'] = 1
    def write_file_check(self)->None:
        self.write_file = True
        if self.dymanic_shell_exec:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF4'] = 1
    def exec_check(self)->None:
        self.dymanic_shell_exec = True
        if self.download:
            self.SPSI_features['BF12'] += 1 
            self.SPSI_features['BF3'] = 1
        if self.read_file:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF5'] = 1
        if self.write_file:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF4'] = 1
    def eval_check(self)->None:
        self.dymanic_source_code_exec = True
        if self.download:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF3'] = 1
        if self.read_file:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF6'] = 1
    def download_upload_check(self)->None:
        self.download = True
        if self.read_file:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF1'] = 1
        if self.dymanic_shell_exec:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF3'] = 1
            self.SPSI_features['BF7'] = 1
        if self.dymanic_source_code_exec:
            self.SPSI_features['BF12'] += 1
            self.SPSI_features['BF3'] = 1
            self.SPSI_features['BF7'] = 1
    def check_shell_commands(self, node:dict)->None:
        if not self.SPSI_features['BF8'] and node.get('arguments') and node.get('arguments')[0].get('value'):
            for shell in self.shells_to_check:
                if shell in node.get('arguments')[0].get('value'):
                    self.SPSI_features['BF8'] = 1
                    break
            for command in self.system_commands_to_check:
                if command in node.get('arguments')[0].get('value'):
                    self.SPSI_features['BF11'] = 1
                    break