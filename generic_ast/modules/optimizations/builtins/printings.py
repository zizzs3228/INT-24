from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import contextlib
import io



class Print_Transformer(BaseTransformer):
    def visit_Call(self, node: ast.Call):
        """
            value=Call(
                func=Name(id='print', ctx=Load()),
                args=[
                Constant(value=b'\n    License: Kortical \xc2\xa9 All rights reserved.\n\nimport zlib,base64\nTfgIBPzCuiebvaVdtjnDMxSoqJcyQWmREGLNHwXFsYhrlKOpAU=base64.b64decode\nTfgIBPzCuiebvaVdtjnDMxSoqJcyQWmREGLNHwXFsYhrlKOpAk=zlib.decompress\nexec(TfgIBPzCuiebvaVdtjnDMxSoqJcyQWmREGLNHwXFsYhrlKOpAk(TfgIBPzCuiebvaVdtjnDMxSoqJcyQWmREGLNHwXFsYhrlKOpAU(\'eJyV0Eeuo2gUBeD5W4X1JlUlt57JoaUaYGNyMNHADMxPzhl21NvolbVLvYJ3x/c7Ojqfn58fp/cp+Qs0I/j7JLfDlL/C6vTvPyemqk5DnmbTeBrACIYFxF8fn2+R19377XRUefRXFI6AwD7yXtgLe3s1k9q1tXcY1fPhlDqzROa8ZsNN4cL4nqRA5n1LY8Wr5P7+X35FBBaDVxuD72eMv/9U+PrD6+5dcfwAG3j9/H7O94n78weQdroaOQs5GCObafxWQvPoTp6xXqBV3Bqrvft8mXbOLat4kc4HRL+KU22xDLzAWtKWsGtZmgTN90KFb3FENSRJQj3pDJeE3IVD0NTbLIqxdpUsCBNX+jF6SO2olt1PkyNanJoKssAv0X60A8tfWueV68C14Wg5P6bBpcFB+QuhVU6iHYi0UKmH4EEGrdTy2Gj9mDFgSxcSxvTeeWT4uZ9xtyZc5QlvZlfyZyZzNEIylJuvYb2zaItdByGnFVkNUivGDC8Z2YpRMQTqZd7tRd+zbntoYpdSEjzWNQheu1odCx6dKWrr1c8d7Fnys8kR8j25oLrFcTbbyGeaJUpWDB2eWkpYz6ikgNE7E8hIUjWhgbu7UBfbe6quI4tbbgiLI+MKTYmmFtYplUzxZRZahETL5oyF4wWQCJJE3T2BybXM0JeHx6SU80kFJ2mI9EkvXlHoVoaOMZCRWM9FRclyjPZtxgzVez8HR+sy5VwJtgV+N1YLRbIw8DkxNlBRVv2BqGfmhnE2xOOStjpEdCFV+C6vZtDlzDqFsr+xqVaGz6uktT3TLkHsBHqVQ2hD7nSbJgjaKxvvYeLAP3YQwFZ2jXGFtAqXXmOQ5BamyzuSIXURmzA2yw9KK6NjGxrGdFKUJ3koRJMcLc9mnUojzvL4Ul7yqlzoh2iA+RmGefzSUZAsra6HUA898acqyIfuIZFYyt3kT1CAN4SbrRZrmd2sxDM1UkNwi03OyHQkFFDxusBBbqsIEz/PvMOrk2xpRrp38NHtMsO5zN32D093lyrE79UMuWO67G4kGzbnS8NejOJWc5nSMLW2LQ7FrYUmcQw56lbBz/kr9+W2b1IiYFbOJDzWT5WLGxsW8jaxkTIEodZSS460bVZNIuzUap4ZoHgbh/749evXx389MZX0\')))\n')],
                keywords=[]))]
        """
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            captured_output = io.StringIO()
            
            args, kwargs, skip = self.args_parser(node.args, node.keywords)
            args = [ar.decode('utf-8') if isinstance(ar, bytes) else ar for ar in args]
            
            if skip:
                return node
            
            with contextlib.redirect_stdout(captured_output):
                print(*args, **kwargs)
            captured = captured_output.getvalue()

            return ast.parse(captured)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "print":
            print("Found print")
