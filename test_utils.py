import ast


def collect_func_def_from_module(module: ast.Module) -> dict[str, ast.FunctionDef]:
    return {
        node.name: node
        for node in module.body
        if isinstance(node, ast.FunctionDef)
    }


def collect_class_def_from_module(module: ast.Module) -> dict[str, ast.ClassDef]:
    return {
        node.name: node
        for node in module.body
        if isinstance(node, ast.ClassDef)
    }


def collect_func_calls_from_func_def(function_node: ast.FunctionDef) -> list[str]:
    names: list[str] = []
    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            called = node.func
            if isinstance(called, ast.Name):
                names.append(called.id)
    return names


def collect_attr_acc_from_func_def(function_node: ast.FunctionDef) -> list[str]:
    names: list[str] = []
    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            called = node.func
            if isinstance(called, ast.Attribute):
                names.append(called.attr)
    return names


def is_float_literal_node(node: ast.AST, value: float) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, (float, int)) and node.value == value


def has_module_constant_value_in_module(module: ast.Module, value: float) -> bool:
    for node in module.body:
        if isinstance(node, ast.Assign) and is_float_literal_node(node.value, value):
            return True
    return False


def has_variable_assignment_in_func_def(
    function_node: ast.FunctionDef,
    variable_name: str,
) -> bool:
    for node in ast.walk(function_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    return True
    return False


def collect_method_from_class_in_module(
    module: ast.Module,
    class_name: str | None = None,
    method_name: str | None = None,
) -> dict[str, ast.FunctionDef] | ast.FunctionDef | None:
    methods: dict[str, ast.FunctionDef] = {}
    for node in module.body:
        if isinstance(node, ast.ClassDef) and (class_name is None or node.name == class_name):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods[item.name] = item
    if method_name is None:
        return methods
    return methods.get(method_name)


def has_return_call_in_func_def(
    function_node: ast.FunctionDef,
    called_name: str,
    first_arg_name: str | None = None,
) -> bool:
    for node in ast.walk(function_node):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Call):
            called = node.value.func
            if not isinstance(called, ast.Name) or called.id != called_name:
                continue
            if first_arg_name is None:
                return True
            if (
                len(node.value.args) >= 1
                and isinstance(node.value.args[0], ast.Name)
                and node.value.args[0].id == first_arg_name
            ):
                return True
    return False
