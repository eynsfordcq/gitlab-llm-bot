import ast
import os 

class FunctionOverviewExtractor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.current_class = None
    
    def visit_ClassDef(self, node):
        # Handle class definitions
        self.current_class = node.name
        self.generic_visit(node)  # Continue visiting to capture methods
        self.current_class = None  # Reset after leaving class

    def visit_FunctionDef(self, node):
        func_name = node.name
        # Extract input arguments
        inputs = [arg.arg for arg in node.args.args]
        
        # Extract output (return statement)
        output = None
        for body_item in node.body:
            if isinstance(body_item, ast.Return):
                output = ast.dump(body_item.value)
                break
        
        # Extract docstring
        docstring = ast.get_docstring(node)

        # Check if inside a class
        full_name = f"{self.current_class}.{func_name}" if self.current_class else func_name
        self.functions.append({
            'name': full_name,
            'inputs': inputs,
            'output': output,
            'docstring': docstring
        })
    
    def extract_from_file(self, file_path):
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        self.visit(tree)
        return self.functions

def get_file_paths(directory):
    file_paths = []
    for dirpath, _, filesnames in os.walk(directory):
        for filename in filesnames:
            if filename.endswith('.py'):
                file_paths.append(os.path.join(dirpath, filename))

    return file_paths

def analyze_repository(repo_path: str):
    overview = {}
    for file in get_file_paths(repo_path):
        extractor = FunctionOverviewExtractor()
        functions = extractor.extract_from_file(file)
        overview[file] = functions
    return overview

def pretty_print_overview(overview):
    for file, functions in overview.items():
        print(f"\nFile: {file}")
        for func in functions:
            name = func['name']
            inputs = ', '.join(func['inputs'])
            output = func['output'] if func['output'] else "None"
            docstring = func['docstring'] if func['docstring'] else "No docstring"
            print(f"  Function/Method: {name}")
            print(f"    Inputs: {inputs}")
            print(f"    Output: {output}")
            print(f"    Docstring: {docstring}")