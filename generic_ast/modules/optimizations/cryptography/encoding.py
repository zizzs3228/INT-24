from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import importlib


class All_encodings(BaseTransformer):
    def visit_Call(self, node: ast.Call):
        '''
            Call(
                func=Attribute(
                    value=Name(id='base64', ctx=Load()),
                    attr='b64decode',
                    ctx=Load()),
                args=[
                    Constant(value='eJyVkkmOo1gUReexilBMMlOU0qaHknIApjeN6ZsZHz626XsDO6pt1MrKqVpBvvE9R1d69+vr6+Pzffozg+0E//68duP8zNL6899/Prm6/hyf98c8fY5wguMK858fX2/i2fTv2OdRP8FfIJ0gRXx4xV3lb8dleUKwpkE+l61gbG43aNluh40jyrqpvCJpih9jfbV6zv/1P/kTUEQOsy6Hf+6ofv2u8PM33vTvitMH3GD2/c89f474379BbQ/OIlw67O7zUCBDIkK12q9nkta61E9j2dwNU+HeotvxqDHUXLsaBPoaa/h2ymirHIqWZIr+lPWIPZ3VU0lreiHU+ulCrd5622EzVKTQNsCD/Mhd1FjaJKZoMcRBWZymI8eHhRNJKsW9BHqP5rsO8Qmt2AGdoyxGi9ujFobDsVImmUyTyHSiHRyObFE9ZsKRvNFIhJMSz6dCsC0CjUFjPbE+chsFCiHzrHhxMl6yJ4W2WKKlmRe087FLLXsi5YsF0mIL7fXWeT21RQMf4PwwrsXMNBGw9HQmqoxQHB25+hi2CfrBhfM1nOQ5ae6eyZ6vEsAl0XQdzS7xXtCgiKuBcDY9oKvDlvf+dOHNCCklyrWwrp7RW7Wbaat112ni1nNEnTlmLsIFBhRzQYnwTt4owPeZxCP28gh86qnEz7N/bRRCFOUx93ZMLtlGkO7ulrnb6kEYesSSsNu8Jxlp12tSF3uyJ4cpqnutLWsMsCNV55zf5VYKKtN/rrJwYRIs7h3D9oYkp2cnRw7Qzl3c565YHqFpP+CCdvllo/JrOI5oxuS01O4TUzlMiZGdPkqZB8Auw1Tz+1DgMRhWfXxQz+puirTIPFS/DB93sNA+XwBIDYtKzADcn7qKGFcvbhppjvvaP7bESdKH6Olkt0vEK7QvmibiHsbvIDLOGlQ2yvWZcyVpWKOyYrVGtdIF7/cZycUJDVZysnovb8m83Y8AHoziINNOBi9tvgeIica6A9QXI1SbWfNOsGL8IBfNoxWxzbLcuezF/CIFyHupySzUhzBI04hsQ5DKB7VUs4d7eqVMvDIENvYQ6NYF2r1Mr9u6xlDnbnhsv6QEKyNZmrkhihrLJvm02Y/FVSPfaQ4O21/s9UqZpbyNci5dfQ2vOkczMj1jm9bvymPVCb+m96E+ugf25BCnkWFxuH7CTWNKKT7HsEyaDbtaLGoixfuMVx564UzCBaOTjE2OTZtgoH5lvp5n3NoVu5IkYVsmngfDpIrH6bYa1lhhW++MPc6YymxMFnmYOCacWbzeR5FmfWMJLYqWiUp+L8FlTFhaWpiRrWvoIabbtDTGfpPZL5KqAX+cqpFFQgyg6jOWgKUJR+iRoS5vU8iU6VZ5qtjliesS1BkEiakuh5/2RNIpd/A40QQL12jDGdZIovO3Hz9+fPwHGt3ySQ==')],
                keywords=[])]
        '''
        if isinstance(node.func, ast.Name):
            if node.func.id in self.variables.keys() and isinstance(self.variables[node.func.id], ast.Attribute):
                method_node = self.variables[node.func.id]
                return ast.Call(func=method_node, args=node.args, keywords=node.keywords)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id in ['base64', 'zlib', 'gzip', 'bz2', 'binascii', 'codecs', 'lzma']:
                module_name = node.func.value.id
                module = importlib.import_module(module_name)
                args, kwargs, skip = self.args_parser(node.args, node.keywords) 
                if skip:
                    return node
                if hasattr(module, node.func.attr):
                    method = getattr(module, node.func.attr)
                    return ast.Constant(value=method(*args, **kwargs))
        
        return node

    def leave_Call(self, node: ast.Call):
        return node