from typing import Any
from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import operator
import re


class Change_name_of_method(BaseTransformer):
    def visit_Name(self, node: ast.Name):
        '''
            Name(id='warnings_filterwarnings', ctx=Store())]
        '''
        if node.id in self.variables_names.keys():
            node.id = self.variables_names[node.id]
        return node
    
class Args_names(BaseTransformer):
    def visit_arg(self, node: ast.arg):
        '''
            arg(arg='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfkoqs')],
        '''
        if node.arg in self.variables_names.keys():
            node.arg = self.variables_names[node.arg]
        return node

class Format_names(BaseTransformer):
    def visit_Attribute(self, node: ast.Attribute):
        '''
            Attribute(
                value=Constant(value='--load-extension={目水鸟月木人木鳥马口马刀木鳥水子}\\Extension'),
                attr='format',
                ctx=Load())
        '''
        if isinstance(node.value, ast.Constant) and node.attr == 'format':
            format_pattern = r'{(.*?)}'
            for found in re.finditer(format_pattern, node.value.value):
                if found.group(1) in self.variables_names.keys():
                    node.value.value = node.value.value.replace(found.group(0), '{' + self.variables_names[found.group(1)] + '}')
        return node

class Keyword_arg(BaseTransformer):
    def visit_keyword(self, node: ast.keyword):
        '''
            keyword(
                arg='目水鸟月木人木鳥马口马刀木鳥水子',
                value=Name(id='funcion_getenv_call', ctx=Load()))]))
        '''
        if node.arg in self.variables_names.keys():
            node.arg = self.variables_names[node.arg]
        return node