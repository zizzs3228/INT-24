from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import contextlib
import io


class Exec(BaseTransformer):
    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id == "exec":
                if len(node.args) == 1 and isinstance(node.args[0], ast.Constant):
                    captured_output = io.StringIO()
                    to_print = node.args[0].value
                    if isinstance(to_print, bytes):
                        to_print = to_print.decode()
                    with contextlib.redirect_stdout(captured_output):
                        print(to_print)
                    captured = captured_output.getvalue()
                    return ast.parse(captured)
        return node

    def leave_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id == "exec":
                return node
        return node

class Eval(BaseTransformer):
    def visit_Call(self, node: ast.Call):
        '''
            Call(
              func=Name(id='eval', ctx=Load()),
              args=[
                Constant(value='magic')],
              keywords=[]),
        '''
        if isinstance(node.func, ast.Name):
            if node.func.id == 'eval':
                if len(node.args)==1:
                    if isinstance(node.args[0], ast.Constant):
                        eval_value = node.args[0].value
                        var_eval = self.variables.get(eval_value)
                        if var_eval and isinstance(var_eval,ast.Constant) and isinstance(var_eval.value, str):
                            return var_eval
                        if isinstance(eval_value, str):
                            print(eval_value)
                            parsed = ast.parse(eval_value)
                            if isinstance(parsed,ast.Module) and isinstance(parsed.body, list):
                                if len(parsed.body)==1 and isinstance(parsed.body[0], ast.Expr):
                                    if isinstance(parsed.body[0].value, ast.Call):
                                        print(parsed.body[0].value,parsed.body[0])
                                        return parsed.body[0].value
        return node


#### Спорно пока что. Не уверен что это нужно

# class Compile(BaseTransformer):
#     def visit_Call(self, node: ast.Call):
#         '''
#             Call(
#                 func=Name(id='compile', ctx=Load()),
#                 args=[
#                 Constant(value=b'print(1)'),
#                 Constant(value='<string>'),
#                 Constant(value='exec')],
#                 keywords=[])]
#         '''
#         if isinstance(node.func, ast.Name):
#             if node.func.id == 'compile':
#                 if len(node.args)==3:
#                     if isinstance(node.args[0], ast.Constant) and isinstance(node.args[1], ast.Constant) and isinstance(node.args[2], ast.Constant):
#                         code = node.args[0].value
#                         filename = node.args[1].value
#                         mode = node.args[2].value
#                         if isinstance(code, bytes):
#                             code = code.decode()
#                         if filename=='<string>' and mode=='exec':
#                             return ast.Constant(value=code)