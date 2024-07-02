from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import builtins

class builtins_transform(BaseTransformer):
    def visit_Call(self, node: ast.Call):
        """
            Call(
            func=Name(id='getattr', ctx=Load()),
            args=[
              Name(id='__builtins__', ctx=Load()),
              Constant(value='chr')],
            keywords=[])
                    """
        '''
        Call(
            func=Name(id='getattr', ctx=Load()),
            args=[
                Name(id='__builtins__', ctx=Load()),
                Constant(value='chr')],
            keywords=[]),
        '''
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id in ('hex', 'oct', 'bin','copyright','credits','license'):
                if isinstance(node.func.attr, str) and node.func.attr in ('__str__'):
                    args,kwargs,skip = self.args_parser(node.args,node.keywords)
                    if skip:
                        return node
                    result = eval(f'{node.func.value.id}.{node.func.attr}(*{args},**{kwargs})')
                    return ast.Constant(value=result)
        elif isinstance(node.func, ast.Name) and node.func.id in ('getattr'):
            if node.args:
                if isinstance(node.args[0], ast.Name) and node.args[0].id == ('__builtins__'):
                    if isinstance(node.args[1], ast.Constant) and node.args[1].value in dir(builtins): 
                        return ast.Name(id=node.args[1].value, ctx=ast.Load())
        return node

class MapCall(BaseTransformer):
    def visit_Call(self, node: ast.Call):
        '''
            Call(
                func=Name(id='map', ctx=Load()),
                args=[
                    Name(id='chr', ctx=Load()),
                    List(
                    elts=[
                        Constant(value=119),
                        Constant(value=105),
                        Constant(value=110),
                        Constant(value=51),
                        Constant(value=50)],
                    ctx=Load())],
                keywords=[])]
        '''
        if isinstance(node.func, ast.Name) and node.func.id == 'map' and node.args:
            if len(node.args) == 2 and isinstance(node.args[0], ast.Name) and isinstance(node.args[1], ast.List):
                args,kwargs,skip = self.args_parser(node.args,node.keywords)
                if skip:
                    return node
                if len(args)==2:
                    if args[0]=='chr' and isinstance(args[1], list):
                        result = list(map(chr,args[1]))
                        return ast.List(elts=[ast.Constant(value=i) for i in result],ctx=ast.Load())
        return node
    
    
class JoinCall(BaseTransformer):
    def visit_Call(self, node: ast.Call):
        '''
            Call(
                func=Attribute(value=Constant(value=''), attr='join', ctx=Load()),
                args=[
                    List(
                    elts=[
                        Constant(value='a'),
                        Constant(value='b'),
                        Constant(value='c')],
                    ctx=Load())],
                keywords=[])
        '''
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Constant) and node.func.attr == 'join' and node.args:
            if len(node.args) == 1 and isinstance(node.args[0], ast.List):
                args,kwargs,skip = self.args_parser(node.args,node.keywords)
                if skip:
                    return node
                if isinstance(node.func.value.value, str):
                    result = node.func.value.value.join(args[0])
                    return ast.Constant(value=result)
        return node
