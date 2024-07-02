from generic_ast.modules.optimizations.base import BaseTransformer
import ast_comments as ast
import operator


class Class_declaration(BaseTransformer):
    def visit_ClassDef(self, node: ast.ClassDef):
        '''
            ClassDef(
                name='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfkosq',
                bases=[
                    Name(id='FileFinder', ctx=Load())],
                keywords=[],
                body=[
                    FunctionDef(
                    name='__init__',
                    args=arguments(
                        posonlyargs=[],
                        args=[
                        arg(arg='self'),
                        arg(arg='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfkoqs')],
                        vararg=arg(arg='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfksGo'),
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]),
                    body=[
                        AugAssign(
                        target=Name(id='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfksGo', ctx=Store()),
                        op=Add(),
                        value=Tuple(
                            elts=[
                            List(
                                elts=[
                                Name(id='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfksGq', ctx=Load()),
                                List(
                                    elts=[
                                    Constant(value='.pye')],
                                    ctx=Load())],
                                ctx=Load())],
                            ctx=Load())),
                        Expr(
                        value=Call(
                            func=Attribute(
                            value=Call(
                                func=Name(id='super', ctx=Load()),
                                args=[],
                                keywords=[]),
                            attr='__init__',
                            ctx=Load()),
                            args=[
                            Name(id='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfkoqs', ctx=Load()),
                            Starred(
                                value=Name(id='YXKAthmSTyUldIpxcCbOeDrNauFVJLgRjvMznQEWPiwHBfksGo', ctx=Load()),
                                ctx=Load())],
                            keywords=[]))],
                    decorator_list=[],
                    type_params=[])],
                decorator_list=[],
                type_params=[]),
        '''
        new_name = self.class_name_generator(node.name)
        node.name = new_name
        return node
    
    
                    
        