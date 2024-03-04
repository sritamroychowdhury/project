from behave import given, when, then
from file_input import field_format_match


@when(u'field format of the extract file is compared with config file')
def step_impl(context):
    context.result = field_format_match(context.df1, context.df3)


@then(u'no unmatched field formats should be found')
def step_impl(context):
    assert context.result == "All field formats are ok", context.result
