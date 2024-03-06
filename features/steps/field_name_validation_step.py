from behave import given, when, then
import pandas as pd
from file_input import field_name_match

# Link to input files

latest_url = r"C:\Users\chowdsr\Desktop\Daily files\IntegriChain_Alexion_Koselugo_Daily_Status_latest.csv"
config_url = r"C:\Users\chowdsr\Desktop\Daily files\Koselugo_status.csv"


@given(u'extract file input')
def step_impl(context):
    context.df1 = latest_url


@given(u'config csv file input')
def step_impl(context):
    context.df3 = config_url


@when(u'field names of the extract file is compared with config file')
def step_impl(context):
    context.result = field_name_match(context.df1, context.df3)


@then(u'no unmatched field names should be found')
def step_impl(context):
    assert context.result == "All the field names are same", context.result
