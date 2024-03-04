from behave import given, when, then
import pandas as pd
from file_input import datatype_match


@when(u'data type of the extract file is compared with config file')
def step_impl(context):
    context.result = datatype_match(context.df1, context.df3)


@then(u'no unmatched data type should be found')
def step_impl(context):
    assert context.result == "All data types are matched", context.result