import ast_comments as ast
import unicodedata
import builtins

entity_types = ("module", "function", "object")


class BaseTransformer(ast.NodeTransformer):
    transforms = None
    calls = 0
    max_calls = 10**9
    variables = {}
    variables_names = {}
    
    
    def new_name_generator(self,new_name:str,var_value:ast.AST,var_name:str)->str:
        counter = 0
        template = new_name
        if var_name in self.variables_names.keys():
            return var_name
        while new_name in self.variables.keys():
            new_name = f"{template}_{counter}"
            counter += 1
            # if var_value == self.variables.get(new_name):
            #     return var_name
        self.variables_names[var_name] = new_name
        return new_name
    
    def classify_characters(self, input_string:str)->dict:
        classes = {
            'lowercase': 0,
            'uppercase': 0,
            'digits': 0,
            'specials': 0,
            'others': 0
        }
        for char in input_string:
            if char.islower():
                class_name = 'lowercase'
            elif char.isupper():
                class_name = 'uppercase'
            elif char.isdigit():
                class_name = 'digits'
            elif unicodedata.category(char).startswith('P'):
                class_name = 'specials'
            else:
                class_name = 'others'
            classes[class_name] += 1
        ratios = {}
        for class_name, count in classes.items():
            ratios[class_name] = count / len(input_string)
        return ratios
    
    def class_name_generator(self, class_name:str)->str:
        ratios = self.classify_characters(class_name)
        if ((ratios['uppercase'] > 0.25 or ratios['specials'] > 0.25 or ratios['others'] > 0.25 or ratios['digits'] > 0.5) and ratios['lowercase']<0.9) or len(class_name) < 4:
            counter = 0
            new_name = f'Class_{counter}'
            if class_name in self.variables_names.keys():
                return class_name
            while new_name in self.variables_names.values():
                new_name = f'Class_{counter}'
                counter += 1
            self.variables_names[class_name] = new_name
            class_name = new_name
        return class_name
    
    def variable_generator(self, var_name:str, var_value:ast.AST)->str:
        ratios = self.classify_characters(var_name)
        if ((ratios['uppercase'] > 0.25 or ratios['specials'] > 0.25 or ratios['others'] > 0.25 or ratios['digits'] > 0.5) and ratios['lowercase']<0.9) or len(var_name) < 4:
            if isinstance(var_value, ast.Attribute):
                method = var_value.value.id
                attr = var_value.attr
                new_name = f"{method}_{attr}"
                result = self.new_name_generator(new_name, var_value, var_name)
                if result == var_name:
                    return var_name
                return result
            
            elif isinstance(var_value, ast.Constant):
                value = var_value.value
                if isinstance(value, str):
                    value_ratios = self.classify_characters(value)
                    if (value_ratios['uppercase'] > 0.4 and value_ratios['lowercase'] > 0.4 and value_ratios['uppercase']+value_ratios['lowercase'] > 0.8) or value.endswith('='):
                        new_name = f'base64_string'
                        result = self.new_name_generator(new_name, var_value, var_name)
                        if result == var_name:
                            return var_name
                        return result
                    
                elif isinstance(value, type(None)):
                    new_name = f'NoneType_variable'
                    result = self.new_name_generator(new_name, var_value, var_name)
                    if result == var_name:
                        return var_name
                    return result
                
                elif isinstance(value, int):
                    new_name = f'int_variable'
                    result = self.new_name_generator(new_name, var_value, var_name)
                    if result == var_name:
                        return var_name
                    return result
            elif isinstance(var_value, ast.Call):
                if isinstance(var_value.func, ast.Attribute):
                    if isinstance(var_value.func.value, ast.Name):
                        method = var_value.func.value.id
                        attr = var_value.func.attr
                        new_name = f"funcion_{attr}_call"
                        result = self.new_name_generator(new_name, var_value, var_name)
                        if result == var_name:
                            return var_name
                        return result
                    elif isinstance(var_value.func.value, ast.Attribute):
                        if isinstance(var_value.func.value.value, ast.Name):
                            method = var_value.func.value.value.id
                            attr = var_value.func.value.attr
                            new_name = f"funcion_{attr}_call"
                            result = self.new_name_generator(new_name, var_value, var_name)
                            if result == var_name:
                                return var_name
                            return result
                elif isinstance(var_value.func, ast.Name):
                    func_id = var_value.func.id
                    new_name = f'result_{func_id}'
                    result = self.new_name_generator(new_name, var_value, var_name)
                    if result == var_name:
                        return var_name
                    return result
            elif isinstance(var_value, ast.Tuple):
                new_name = f'tuple_variable'
                result = self.new_name_generator(new_name, var_value, var_name)
                if result == var_name:
                    return var_name
                return result
            elif isinstance(var_value, ast.BinOp):
                new_name = f'binop_variable'
                result = self.new_name_generator(new_name, var_value, var_name)
                if result == var_name:
                    return var_name
                return result
            elif isinstance(var_value, ast.Name):
                new_name = f'iter_variable'
                result = self.new_name_generator(new_name, var_value, var_name)
                if result == var_name:
                    return var_name
                return result
            elif isinstance(var_value, ast.List):
                new_name = f'list_variable'
                result = self.new_name_generator(new_name, var_value, var_name)
                if result == var_name:
                    return var_name
                return result
            elif isinstance(var_value, ast.arguments):
                if var_value.vararg and isinstance(var_value.vararg, ast.arg) and var_value.vararg.arg == var_name:
                    new_name = f'vararg_variable'
                    result = self.new_name_generator(new_name, var_value, var_name)
                    if result == var_name:
                        return var_name
                    return result                    

                    
        return var_name
                
        
    
    def args_parser(self, args: list[ast.AST], keywords: list[ast.keyword]) -> tuple[list, dict, bool]:
        skip = False
        args_for_method = []
        kwargs_for_method = {}
        for arg in args:
            if isinstance(arg, ast.Call):
                skip = True
                break
            elif isinstance(arg, ast.BinOp):
                skip = True
                break
            elif isinstance(arg, ast.Constant):
                args_for_method.append(arg.value)
            elif isinstance(arg, ast.Name):
                value = self.variables.get(arg.id)
                if value and isinstance(value, ast.Constant):
                    args_for_method.append(value.value)
                elif arg.id in dir(builtins):
                    args_for_method.append(arg.id)
            elif isinstance(arg, ast.List):
                list_values = []
                for value in arg.elts:
                    if isinstance(value, ast.Constant):
                        list_values.append(value.value)
                if len(list_values) == len(arg.elts):
                    args_for_method.append(list_values)
                else:
                    skip = True
                    break
            
                    
        if not skip:
            for keyword in keywords:
                if isinstance(keyword.value, ast.Call):
                    skip = True
                    break
                elif isinstance(keyword.value, ast.BinOp):
                    skip = True
                    break
                elif isinstance(keyword.value, ast.Constant):
                    kwargs_for_method[keyword.arg] = keyword.value.value
                elif isinstance(keyword.value, ast.Name):
                    value = self.variables.get(keyword.value.id)
                    if value and isinstance(value, ast.Constant):
                        kwargs_for_method[keyword.arg] = value.value
                    elif keyword.value.id in dir(builtins):
                        kwargs_for_method[keyword.arg] = keyword.value.id
                elif isinstance(keyword.value, ast.List):
                    list_values = []
                    for value in keyword.value.elts:
                        if isinstance(value, ast.Constant):
                            list_values.append(value.value)
                    if len(list_values) == len(keyword.value.elts):
                        kwargs_for_method[keyword.arg] = list_values
                    else:
                        skip = True
                        break
        
        return args_for_method, kwargs_for_method, skip
    
    def visit(self, node):
        BaseTransformer.calls += 1
        if BaseTransformer.calls > BaseTransformer.max_calls:
            return node
     
        # if self.transforms is not None:
        #     for transform in self.transforms:
        
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor:
            new_node = visitor(node)
            if new_node != node and new_node is not None:
                node = new_node

        node_cand = self.generic_visit(node)
        if node_cand is not None:
            node = node_cand

        # if self.transforms is not None:
        #     for transform in self.transforms:
        method = 'leave_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor:
            new_node = visitor(node)
            if new_node != node and new_node is not None:
                node = new_node

        return node

    def generic_visit(self, node):
        for field, old_value in ast.iter_fields(node):
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, ast.AST):
                        value = self.visit(value)
                        if value is None:
                            continue
                        elif not isinstance(value, ast.AST):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, ast.AST):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node

    def generic_leave(self, node):
        return node
