import ast
import multiprocessing
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class ExecuteCodeInput(BaseModel):
    code: str = Field(description="The exact python code to execute. Can be multiple lines. Output should be captured via variable assignments or implicitly returned.")

def _run_sandbox(code: str, queue: multiprocessing.Queue):
    """Inner function to run code using process isolation."""
    try:
        # Simple sandbox environment
        local_scope = {}
        
        # Parse first to catch syntax errs
        parsed_ast = ast.parse(code)
        
        # We can extract the last expression to automatically return it
        if isinstance(parsed_ast.body[-1], ast.Expr):
            last_expr = parsed_ast.body.pop()
            exec(compile(parsed_ast, '<string>', 'exec'), {}, local_scope)
            res = eval(compile(ast.Expression(last_expr.value), '<string>', 'eval'), {}, local_scope)
            queue.put({"status": "success", "result": res})
        else:
            exec(code, {}, local_scope)
            queue.put({"status": "success", "result": "Code executed successfully. Local scope variables: " + str(list(local_scope.keys()))})
    except Exception as e:
        queue.put({"status": "error", "error": str(e)})

@tool("execute_code", args_schema=ExecuteCodeInput)
def execute_code(code: str) -> str:
    """Evaluates Python code in a sandboxed process with a strict 5-second timeout."""
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_run_sandbox, args=(code, queue))
    process.start()
    
    # 5 second timeout for safety
    process.join(5)
    
    if process.is_alive():
        process.terminate()
        process.join()
        return "Error: Execution timed out after 5 seconds."
        
    try:
        result = queue.get_nowait()
        if result["status"] == "success":
            return f"Success: {result['result']}"
        else:
            return f"Error: {result['error']}"
    except Exception:
        return "Error: Unrecognized execution failure."
