from behave import given, when, then
import pandas as pd
from file_input import row_count


@when(u'row count of the files are compared')
def step_impl(context):
    context.count = row_count(context.df1, context.df2)


@then(u'row count should be equal')
def step_impl(context):
    assert context.count == "No of rows in both files are same", context.count
