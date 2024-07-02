import ast
import traceback
import logzero

import generic_ast.modules.optimizations


def optimizer(my_ast):
    # делаем до тех пор, пока можно хоть что-то оптимизировать
    is_loop_opted = True
    iter_num = 0
    while is_loop_opted:
        print("iteration", iter_num)
        iter_num += 1
        before_dump = ast.dump(my_ast)
        is_loop_opted = False

        for opt in generic_ast.modules.optimizations.BaseTransformer.__subclasses__():
            try:
                print("Processing", opt)
                opt_object = opt()
                my_ast = ast.fix_missing_locations(opt_object.visit(my_ast))

            except Exception:
                print("Failed", opt)
                print(">>>")
                traceback.print_exc()
                print("<<<")


        if before_dump != ast.dump(my_ast):
            is_loop_opted = True
    print("Done in", generic_ast.modules.optimizations.BaseTransformer.calls, "calls")
    generic_ast.modules.optimizations.BaseTransformer.variables = {}
    generic_ast.modules.optimizations.BaseTransformer.variables_names = {}
    generic_ast.modules.optimizations.BaseTransformer.calls = 0
    return my_ast


