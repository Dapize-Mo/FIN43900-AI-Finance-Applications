import ast
from pathlib import Path

source_path = Path(__file__).with_name("create_video2_video3_scripts.py")
source = source_path.read_text(encoding="utf-8")
tree = ast.parse(source)
function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "make_pdf")
namespace = {}
exec("\n".join(source.splitlines()[:function.end_lineno]), namespace)
video3_call = next(
    node
    for node in tree.body
    if isinstance(node, ast.Expr)
    and isinstance(node.value, ast.Call)
    and "video-3" in ast.unparse(node.value.args[0])
)
exec(compile(ast.Module(body=[video3_call], type_ignores=[]), str(source_path), "exec"), namespace)
