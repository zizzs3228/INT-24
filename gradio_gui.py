import gradio as gr
from generic_ast.main import *

def deob(source):
    try:
        ast = ast_lib.parse(source=source, filename='<unknown>', type_comments=True)
    except:
        return "", "", "Failed to parse AST"
    ast_before = ast_lib.dump(ast, indent=2)
    new_ast = modules_optimize.optimizer(ast)
    ast_after = ast_lib.dump(new_ast, indent=2)
    try:
        unparse = ast_lib.unparse(new_ast)
    except:
        unparse = "Failed to unparse ast"

    return ast_before, ast_after, unparse

def app():
    with gr.Blocks() as demo:
        code = gr.Code(lines=5, language="python", label="Input code",
                       value="import dis; dis.dis('a=0')")
        greet_btn = gr.Button("Deobfuscate!")
        deobfed = gr.Code(language="python", label="AST Deobfed")
        with gr.Row():
            ast_before = gr.Code(language="python", label="AST before")
            ast_after = gr.Code(language="python", label="AST after")

        greet_btn.click(fn=deob, inputs=code, outputs=[ast_before, ast_after, deobfed], api_name="disassembly")

    demo.launch(server_name='0.0.0.0')


if __name__ == "__main__":
    app()