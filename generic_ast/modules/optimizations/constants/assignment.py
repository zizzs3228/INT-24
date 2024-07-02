from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import operator


class Method_Asign(BaseTransformer):
    def visit_Assign(self, node: ast.Assign):
        '''
            Assign(
                targets=[
                Name(id='TfgIBPzCuiebvaVdtjnDMxSoqJcyQWmREGLNHwXFsYhrlKOpAU', ctx=Store())],
                value=Attribute(
                value=Name(id='base64', ctx=Load()),
                attr='b64decode',
                ctx=Load())),
        '''
        if node.targets:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    var_value = node.value
                    var_name = self.variable_generator(var_name, var_value)
                    self.variables[var_name] = var_value
                    target.id = var_name
        return node

class Functiondef_args_visit(BaseTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        '''
            FunctionDef(
                name='__init__',
                args=arguments(
                    posonlyargs=[],
                    args=[
                    arg(arg='self'),
                    arg(arg='funcion_get_filename_call')],
                    vararg=arg(arg='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfksGo'),
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[]),
        '''
        if node.args and node.args.vararg:
            print(node.args.vararg.arg)
            var_name = node.args.vararg.arg
            var_value = node.args
            var_name = self.variable_generator(var_name, var_value)
            node.args.vararg.arg = var_name
        return node

### Заменил на другую реализацию
# class AugAssign(BaseTransformer):
#     def visit_AugAssign(self, node: ast.AugAssign):
#         '''
#         AugAssign(
#             target=Name(id='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfksGo', ctx=Store()),
#             op=Add(),
#             value=Tuple(
#                 elts=[
#                 List(
#                     elts=[
#                     Name(id='Class_0', ctx=Load()),
#                     List(
#                         elts=[
#                         Constant(value='.pye')],
#                         ctx=Load())],
#                     ctx=Load())],
#                 ctx=Load()))
#         '''
        # if isinstance(node.target, ast.Name):
            # var_name = node.target.id
            # var_value = node.value
            # var_name = self.variable_generator(var_name, var_value)
            # self.variables[var_name] = var_value
            # node.target.id = var_name
            


