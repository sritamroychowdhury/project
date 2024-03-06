from behave import given, when, then
import pandas as pd
from file_input import column_name_match

# Link of the files

last_week_url = r"C:\Users\chowdsr\Desktop\Daily files\IntegriChain_Alexion_Koselugo_Daily_Status_lastweek.csv"
latest_url = r"C:\Users\chowdsr\Desktop\Daily files\IntegriChain_Alexion_Koselugo_Daily_Status_latest.csv"



@given(u'last week csv file input')
def step_impl(context):
    context.df1 = last_week_url


@given(u'latest csv file input')
def step_impl(context):
    context.df2 = latest_url


@when(u'column names of the files are compared')
def step_impl(context):
    context.result = column_name_match(context.df1, context.df2)


@then(u'no unmatched column names should be found')
def step_impl(context):
    assert context.result == "All the column names are same", context.result
