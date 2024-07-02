import sys
import os
import ast_comments as ast_lib
import logzero
import generic_ast.modules.optimize as modules_optimize

logger = logzero.setup_default_logger()



sys.setrecursionlimit(sys.getrecursionlimit()*1000)


def deob(source, filename='<unknown>'):
    ast = ast_lib.parse(source=source, filename=filename, type_comments=True)
    #logger.debug(ast_lib.dump(ast, indent=4))
    new_ast = modules_optimize.optimizer(ast)
    #logger.debug(ast_lib.dump(new_ast, indent=2))
    return ast_lib.unparse(new_ast)


def usage():
    print(f"Usage: {os.path.basename(sys.argv[0])} python_code.py")

def main():
    if len(sys.argv) != 2:
        return usage()
    with open(sys.argv[1], "rb") as f:
        new_code = deob(f.read(), filename=sys.argv[1])
        logger.debug("Return ast:\n" + new_code)

if __name__ == "__main__":
    main()

