from datetime import datetime
import re
import pandas as pd
import csv


# IntegriChain_Alexion_Koselugo_Daily_Status_lastweek.csv
# IntegriChain_Alexion_Koselugo_Daily_Status_latest.csv
# Koselugo_status.csv

def column_name_match(file1, file2):
    lastweek_name = file1.split('\\')
    lastweek_name = lastweek_name[-1].rstrip(".csv")
    latest_name = file2.split('\\')
    latest_name = latest_name[-1].rstrip(".csv")

    file1 = pd.read_csv(file1)
    file2 = pd.read_csv(file2)
    pass_dict = dict()
    columnname_extract_lastweek = file1.axes[1].tolist()
    columnname_extract_latest = file2.axes[1].tolist()
    all_columns = set(columnname_extract_lastweek + columnname_extract_latest)
    a = [i for i in columnname_extract_lastweek if i not in columnname_extract_latest]  # missing in latest
    b = [j for j in columnname_extract_latest if j not in columnname_extract_lastweek]  # missing in lastweek

    test_results = []
    for column in all_columns:
        if column in a:
            result = {
                'Column_name': column,
                'Lastweek extract file': "Present",
                'Latest extract file': "Missing",
                'Status': "Failed",
                'Note': "Missing in latest extract file"
            }

        elif column in b:
            result = {
                'Column_name': column,
                'Lastweek extract file': "Missing",
                'Latest extract file': "Present",
                'Status': "Failed",
                'Note': "Missing in lastweek extract file"
            }

        else:
            result = {
                'Column_name': column,
                'Lastweek extract file': "Present",
                'Latest extract file': "Present",
                'Status': "Pass",
                'Note': "No error"
            }

        test_results.append(result)

    csv_file = 'column_name_results.csv'
    fieldnames = ['Column_name', 'Lastweek extract file', 'Latest extract file', 'Status', 'Note']
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write results row by row
        for result in test_results:
            writer.writerow(result)

    pass_dict['Columns missing in Latest'] = a
    if len(a) != 0:
        return pass_dict
    else:
        return "All the column names are same"


def row_count(file1, file2):
    lastweek_name = file1.split('\\')
    lastweek_name = lastweek_name[-1].rstrip(".csv")
    latest_name = file2.split('\\')
    latest_name = latest_name[-1].rstrip(".csv")
    file1 = pd.read_csv(file1)
    file2 = pd.read_csv(file2)

    rowcount_lastweek = len(file1)
    rowcount_latest = len(file2)
    count = rowcount_latest - rowcount_lastweek

    test_results = []
    if count == 0:
        result = {
            lastweek_name: len(file2),
            latest_name: len(file1),
            'Status': "Pass",
            'Note': "No error"
        }

    elif count > 0:
        result = {
            lastweek_name: len(file2),
            latest_name: len(file1),
            'Status': "Failed",
            'Note': "No of rows in latest file is more"
        }

    else:
        result = {
            lastweek_name: len(file2),
            latest_name: len(file1),
            'Status': "Failed",
            'Note': "No of rows in lastweek file is more"
        }

    test_results.append(result)

    csv_file = 'row_count_results.csv'
    fieldnames = [lastweek_name, latest_name, 'Status', 'Note']
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write results row by row
        for result in test_results:
            writer.writerow(result)

    if count != 0:
        return "No of rows mismatched", count
    else:
        return "No of rows in both files are same"


def field_name_match(file1, file2):
    extract_name = file1.split('\\')
    extract_name = extract_name[-1].rstrip(".csv")
    config_name = file2.split('\\')
    config_name = config_name[-1].rstrip(".csv")

    file1 = pd.read_csv(file1)
    file2 = pd.read_csv(file2)

    pass_dict = dict()
    fieldname = file2["Field Name"].tolist()
    columnname_extract = file1.axes[1].tolist()
    all_columns = set(fieldname + columnname_extract)
    a = [i for i in columnname_extract if i not in fieldname]  # missing in config
    b = [j for j in fieldname if j not in columnname_extract]  # missing in extract

    test_results = []
    for column in all_columns:
        if column in a:
            result = {
                'Column_name': column,
                'Extract file': "Present",
                'Config file': "Missing",
                'Status': "Failed",
                'Note': "Missing in config file"
            }

        elif column in b:
            result = {
                'Column_name': column,
                'Extract file': "Missing",
                'Config file': "Present",
                'Status': "Failed",
                'Note': "Missing in extract file"
            }

        else:
            result = {
                'Column_name': column,
                'Extract file': "Present",
                'Config file': "Present",
                'Status': "Pass",
                'Note': "No error"
            }

        test_results.append(result)

    csv_file = extract_name + '_field_name_results.csv'
    fieldnames = ['Column_name', 'Extract file', 'Config file', 'Status', 'Note']
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write results row by row
        for result in test_results:
            writer.writerow(result)

    pass_dict['Columns missing in Latest'] = a
    if len(pass_dict) != 0:
        return pass_dict
    else:
        return "All the column names are same"


def field_format_match(file1, file2):
    extract_name = file1.split('\\')
    extract_name = extract_name[-1].rstrip(".csv")
    config_name = file2.split('\\')
    config_name = config_name[-1].rstrip(".csv")

    extract = pd.read_csv(file1)
    config_df = pd.read_csv(file2)

    config_df = config_df.loc[0::, ['Field Name', 'Field Format', 'Requirement', 'Data Type']]
    dict_df = config_df.set_index('Field Name')[['Field Format', 'Requirement', 'Data Type']].to_dict()

    pass_dict = dict()

    def validate_fieldformat(pattern, test_str):

        # initializing format
        if pattern == "YYYY":
            format = "%Y"
            if bool(datetime.strptime(str(test_str), format)):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "YYYYMMDD":
            pattern_str = "^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$"
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "YYYYMMDDHHMMSS":
            pattern_str = ("^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])([01][0-9]|2[0-4])([012345][0-9]|6[0])(["
                           "012345][0-9]|6[0])$")
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "YYYYMMDD HH:MM:SS":
            pattern_str = ("^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-4]):([012345][0-9]|6[0]):("
                           "[012345][0-9]|6[0])$")
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "2 chars":
            my_reg_exp = "^[a-zA-Z]{2}$"
            if re.match(my_reg_exp, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "3 digits":
            my_reg_exp = "^[0-9]{3}$"
            if re.match(my_reg_exp, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "No dashes":
            my_reg_exp = "[-]"
            if re.match(my_reg_exp, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

    test_results = []
    for key in dict_df['Field Format'].keys():
        if dict_df['Data Type'][key] == 'DATE(8)':
            extract[key] = extract[key].astype('Int64')
        pass_lst = []
        if key not in extract.columns:
            continue
        else:
            for row_index, row in extract[key].items():
                if pd.isnull(dict_df['Field Format'][key]):
                    dict_df['Field Format'][key] = ""
                if pd.isnull(row):
                    if dict_df['Requirement'][key] == 'Y':
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': "",
                            'Field format': dict_df['Field Format'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': "Failed",
                            'Note': "Data not provided"
                        }
                    else:
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': "",
                            'Field format': dict_df['Field Format'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': "Pass",
                            'Note': "Data not provided"
                        }

                elif dict_df['Requirement'][key] == 'Y':
                    if dict_df['Field Format'][key] == "":
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': row,
                            'Field format': dict_df['Field Format'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': "Failed",
                            'Note': "Field format not provided"
                        }
                    else:
                        format = dict_df['Field Format'][key]
                        x = validate_fieldformat(format, str(row))
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': row,
                            'Field format': dict_df['Field Format'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': 'Pass' if x == True else 'Failed',
                            'Note': 'No error' if x == True else 'Field format mismatched'
                        }

                else:
                    result = {
                        'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                        'Field_name': key,
                        'Value': row,
                        'Field format': dict_df['Field Format'][key],
                        'Required': dict_df['Requirement'][key],
                        'Status': "Pass",
                        'Note': "No error"
                    }

                if not x:
                    pass_lst.append(x)

                test_results.append(result)

        if len(pass_lst) != 0:
            pass_dict[key] = pass_lst

    csv_file = extract_name + '_field_format_results.csv'
    fieldnames = ['Pharmacy_transaction_id','Field_name', 'Value','Field format','Required','Status', 'Note']
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write results row by row
        for result in test_results:
            writer.writerow(result)

    if len(pass_dict) == 0:
        return "All field formats are ok"
    else:
        return "There are some errors in the field format", pass_dict


def datatype_match(file1, file2):
    extract_name = file1.split('\\')
    extract_name = extract_name[-1].rstrip(".csv")
    config_name = file2.split('\\')
    config_name = config_name[-1].rstrip(".csv")

    extract = pd.read_csv(file1)
    config_df = pd.read_csv(file2)
    config_df = config_df.loc[0::, ['Field Name', 'Data Type', 'Requirement']]
    dict_df = config_df.set_index('Field Name')[['Data Type', 'Requirement']].to_dict()
    for key in dict_df['Data Type']:
        if dict_df['Data Type'][key] == 'DATE(8)':
            extract[key] = extract[key].astype('Int64')

    pass_dict = dict()

    def datatype_validate(pattern, test_str):

        if pattern == "DATE(8)":
            format = "%Y%m%d"
            if len(str(test_str)) == 8:
                if bool(datetime.strptime(str(test_str), format)):
                    return True
            else:
                return str(test_str)

        elif pattern == "TIMESTAMP":
            format = "%Y%m%d %H:%M:%S"
            if bool(datetime.strptime(str(test_str), format)):
                return True
            else:
                return str(test_str)

        elif pattern == "VARCHAR(1)":
            if len(test_str) <= 1:
                if isinstance(test_str, str) or isinstance(test_str, int):
                    return True
            else:
                return str(test_str)

        elif pattern == "VARCHAR(256)":
            if len(test_str) <= 256:
                if isinstance(test_str, str) or isinstance(test_str, int):
                    return True
            else:
                return str(test_str)

        elif pattern == "NUMERIC(11, 2)":
            my_reg_exp = "^[0-9]{0,11}(\.[0-9]{0,2})?$"
            if re.match(my_reg_exp, str(test_str)):
                if isinstance(test_str, float):
                    return True
            else:
                return str(test_str)

        elif pattern == "INTEGER":
            if isinstance(test_str, int):
                return True
            else:
                return str(test_str)

    test_results = []
    for key in dict_df['Data Type'].keys():
        # if pd.isnull(dict_df['Data Type'][key]):
        #   dict_df['Data Type'][key] = "Null"
        pass_lst = []
        if key not in extract.columns:
            continue
        else:
            for row_index, row in extract[key].items():
                if pd.isnull(row):
                    if dict_df['Requirement'][key] == 'Y':
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': "",
                            'Data type': dict_df['Data Type'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': "Failed",
                            'Note': "Data not provided"
                        }
                    else:
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': "",
                            'Data type': dict_df['Data Type'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': "Pass",
                            'Note': "Data not provided"
                        }

                else:
                    format = dict_df['Data Type'][key]
                    x = datatype_validate(format, str(row))
                    if pd.isnull(dict_df['Data Type'][key]):
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': row,
                            'Data type': "",
                            'Required': dict_df['Requirement'][key],
                            'Status': 'Pass' if x == True else 'Failed',
                            'Note': 'No error' if x == True else 'Datatype mismatched'
                        }
                    else:
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': row,
                            'Data type': dict_df['Data Type'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': 'Pass' if x == True else 'Failed',
                            'Note': 'No error' if x == True else 'Datatype mismatched'
                        }

                        if not x:
                            pass_lst.append(x)

                test_results.append(result)

        if len(pass_lst) != 0:
            pass_dict[key] = pass_lst

    csv_file = extract_name + '_datatype_results.csv'
    fieldnames = ['Pharmacy_transaction_id', 'Field_name', 'Value','Data type','Required','Status', 'Note']
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write results row by row
        for result in test_results:
            writer.writerow(result)

    if len(pass_dict) == 0:
        return "All data types are matched"
    else:
        return "There is some error with the data type of these values: ", pass_dict


def expected_values_match(file1, file2):
    extract_name = file1.split('\\')
    extract_name = extract_name[-1].rstrip(".csv")
    config_name = file2.split('\\')
    config_name = config_name[-1].rstrip(".csv")

    extract = pd.read_csv(file1)
    config_df = pd.read_csv(file2)

    config_df = config_df.loc[0::, ['Field Name', 'Expected Value/s (comma separated)', 'Requirement', 'Data Type']]
    dict_df = config_df.set_index('Field Name')[
        ['Expected Value/s (comma separated)', 'Requirement', 'Data Type']].to_dict()

    pass_dict = dict()
    test_results = []
    for key in dict_df['Expected Value/s (comma separated)'].keys():
        if dict_df['Data Type'][key] == 'DATE(8)':
            extract[key] = extract[key].astype('Int64')
        pass_lst = []
        if key not in extract.columns:
            continue
        else:
            if pd.isnull(dict_df['Expected Value/s (comma separated)'][key]):
                dict_df['Expected Value/s (comma separated)'][key] = ""
                # print(dict_df[key])
            for row_index, row in extract[key].items():
                if pd.isnull(row):
                    if dict_df['Requirement'][key] == 'Y':
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': "",
                            'Expected_Values': dict_df['Expected Value/s (comma separated)'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': "Failed",
                            'Note': "Data not provided"
                        }
                    else:
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': "",
                            'Expected_Values': dict_df['Expected Value/s (comma separated)'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': "Pass",
                            'Note': "Data not provided"
                        }

                elif dict_df['Requirement'][key] == 'Y':
                    if str(row) in dict_df['Expected Value/s (comma separated)'][key]:
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': row,
                            'Expected_Values': dict_df['Expected Value/s (comma separated)'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': 'Pass',
                            'Note': 'No error'
                        }
                    else:
                        result = {
                            'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                            'Field_name': key,
                            'Value': row,
                            'Expected_Values': dict_df['Expected Value/s (comma separated)'][key],
                            'Required': dict_df['Requirement'][key],
                            'Status': 'Failed',
                            'Note': 'Expected values mismatched'
                        }

                else:
                    result = {
                        'Pharmacy_transaction_id': extract['PHARMACY_TRANSACTION_ID'][row_index],
                        'Field_name': key,
                        'Value': row,
                        'Expected_Values': dict_df['Expected Value/s (comma separated)'][key],
                        'Required': dict_df['Requirement'][key],
                        'Status': 'Pass',
                        'Note': 'Expected values mismatched'
                    }

                test_results.append(result)

        if len(pass_lst) != 0:
            pass_dict[key] = pass_lst

    csv_file = extract_name + '_expected_value_results.csv'
    fieldnames = ['Pharmacy_transaction_id','Field_name', 'Value','Expected_Values','Required', 'Status', 'Note']
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write headers
        writer.writeheader()

        # Write results row by row
        for result in test_results:
            writer.writerow(result)
    if len(pass_dict) == 0:
        return "All expected values are matched"
    else:
        return "There is some error with the expected values of these values: ", pass_dict
