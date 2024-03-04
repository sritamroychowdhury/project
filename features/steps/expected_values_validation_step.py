from behave import given, when, then
from file_input import expected_values_match


@when(u'expected values of the extract file is compared with config file')
def step_impl(context):
    context.result = expected_values_match(context.df1, context.df3)


@then(u'no unmatched expected values should be found')
def step_impl(context):
    assert context.result == "All expected values are matched", context.result