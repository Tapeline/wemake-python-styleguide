import pytest

from wemake_python_styleguide.violations.complexity import (
    TooComplexFormattedStringViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import (
    WrongFormatStringVisitor,
    WrongStringVisitor,
)

regular_string = "'some value'"
binary_string = "b'binary'"
unicode_string = "u'unicode'"
string_variable = "some = '123'"
formatted_string = "'x + y = {0}'.format(2)"
key_formatted_string = "'x + y = {res}'.format(res=2)"
variable_format = """
some = 'x = {0}'
some.format(2)
"""

# Allowed
f_single_chained_attr = "f'{attr1.attr2}'"
f_variable_lookup = "f'smth {value}'"
f_dict_lookup_str_key = 'f\'smth {dict_value["key"]}\''
f_list_index_lookup = "f'smth {list_value[0]}'"
f_function_empty_args = "f'smth {user.get_full_name()}'"
f_attr_on_function = "f'{fcn().attr}'"
f_true_index = "f'{array[True]}'"
f_none_index = "f'{array[None]}'"
f_byte_index = 'f\'{array[b"Hello"]}\''
f_empty_string = "f''"
f_function_with_single_arg = "f'smth {func(arg)}'"
f_function_with_three_args = "f'{func(arg1, arg2, arg3)}'"
f_method_with_three_args = "f'{obj.method(arg1, arg2, arg3)}'"

# Disallowed
f_string = "f'x + y = {2 + 2}'"
f_double_indexing = "f'{list[0][1]}'"
f_calling_returned_function = "f'{calling_returned_function()()}'"
f_complex_f_string = """
    f'{reverse(\"url-name\")}?{\"&\".join(\"user=\"+uid for uid in user_ids)}'
"""
f_dict_lookup_function_empty_args = "f'smth {dict_value[func()]}'"
f_list_slice_lookup = "f'smth {list[:]}'"
f_attr_on_returned_value = "f'{some.call().attr}'"
f_function_on_attr = "f'{some.attr.call()}'"
f_array_object = "f'{some.first[0].attr.other}'"
f_double_chained_attr = "f'{attr1.attr2.attr3}'"
f_triple_call = "f'{foo()()()}'"
f_triple_lookup = "f'{arr[0][1][2]}'"
f_double_call_arg = "f'{foo()(arg)}'"
f_single_chained_functions = "f'{f1().f2()}'"
f_function_with_four_args = "f'{func(arg1, arg2, arg3, arg4)}'"
f_method_with_four_args = "f'{obj.meth(arg1, arg2, arg3, arg4)}-post'"

# regression 1921
f_string_comma_format = 'f"Count={count:,}"'


@pytest.mark.parametrize(
    'code',
    [
        regular_string,
        binary_string,
        unicode_string,
        string_variable,
        formatted_string,
        key_formatted_string,
        variable_format,
    ],
)
def test_string_normal(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that regular strings work well."""
    tree = parse_ast_tree(code)

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        f_complex_f_string,
        f_dict_lookup_function_empty_args,
        f_string,
        f_list_slice_lookup,
        f_attr_on_returned_value,
        f_function_on_attr,
        f_array_object,
        f_double_chained_attr,
        f_triple_call,
        f_triple_lookup,
        f_double_call_arg,
        f_double_indexing,
        f_calling_returned_function,
        f_single_chained_functions,
        f_function_with_four_args,
    ],
)
def test_complex_f_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that complex ``f`` strings are not allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongFormatStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [TooComplexFormattedStringViolation],
    )


@pytest.mark.parametrize(
    'code',
    [
        f_dict_lookup_str_key,
        f_function_empty_args,
        f_list_index_lookup,
        f_variable_lookup,
        f_single_chained_attr,
        f_attr_on_function,
        f_true_index,
        f_none_index,
        f_byte_index,
        f_string_comma_format,
        f_empty_string,
        f_function_with_single_arg,
        f_function_with_three_args,
        f_method_with_three_args,
    ],
)
def test_simple_f_string(assert_errors, parse_ast_tree, code, default_options):
    """Testing that non complex ``f`` strings are allowed."""
    tree = parse_ast_tree(code)

    visitor = WrongFormatStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
