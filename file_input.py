from datetime import datetime
import re
import pandas as pd


# IntegriChain_Alexion_Koselugo_Daily_Status_lastweek.csv
# IntegriChain_Alexion_Koselugo_Daily_Status_latest.csv
# Koselugo_status.csv

def column_name_match(file1, file2):
    pass_dict = dict()
    columnname_lastweek = file1.axes[1]
    columnname_latest = file2.axes[1]
    mismatch1 = [i for i in columnname_latest if i not in columnname_lastweek]
    mismatch2 = [i for i in columnname_lastweek if i not in columnname_latest]
    if len(mismatch1) != 0:
      pass_dict['Last week'] = mismatch1
    elif len(mismatch2) != 0:
      pass_dict['Latest'] = mismatch2
    if len(pass_dict) !=0:
      return "Columns missing in: ", pass_dict
    else:
      return "All the column names are same"


def row_count(file1, file2):
    columcount_latest = len(file1)
    columncount_lastweek = len(file2)
    count = columcount_latest - columncount_lastweek
    if count != 0:
        return "No of rows mismatched", count
    else:
        return "No of rows in both files are same"


def field_name_match(file1, file2):
    pass_dict = dict()
    fieldname = file2["Field Name"].tolist()
    columnname_extract = file1.axes[1]
    a = [i for i in columnname_extract if i not in fieldname]
    pass_dict['Fields missing in Latest'] = a
    if len(pass_dict) !=0:
      return pass_dict
    else:
      return "All the field names are same"


def field_format_match(file1, file2):
    extract_df = file1
    config_df = file2
    config_df = config_df.loc[0::, ['Field Name', 'Field Format']]
    config_df = config_df.dropna()
    dict_df = config_df.set_index('Field Name')['Field Format'].to_dict()
    # dict_df.pop("SHIP_DATE")

    extract_df["REFERRAL_DATE"] = extract_df["REFERRAL_DATE"].astype('Int64')
    extract_df["PATIENT_CONSENT_DATE"] = extract_df["PATIENT_CONSENT_DATE"].astype('Int64')
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
            pattern_str = "^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])([01][0-9]|2[0-4])([012345][0-9]|6[0])([012345][0-9]|6[0])$"
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "YYYYMMDD HH:MM:SS":
            pattern_str = "^[0-9]{4}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-4]):([012345][0-9]|6[0]):([012345][0-9]|6[0])$"
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "2 chars":
            pattern_str = "^[a-zA-Z]{2}$"
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

        elif pattern == "3 digits":
            pattern_str = "^[0-9]{3}$"
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)


        elif pattern == "No dashes":
            pattern_str = "[-]"
            if re.match(pattern_str, test_str):
                return True
                # print(test_str)
                # return str(test_str)
            else:
                return str(test_str)

    for key in dict_df.keys():
        if key not in extract_df.columns:
            continue
        else:
            for row in extract_df[key]:
                pass_lst = []
                if pd.isnull(row):
                    continue
                else:
                    format = dict_df[key]
                    x = validate_fieldformat(format, str(row))
                    if x != True:
                        pass_lst.append(x)

                if len(pass_lst) != 0:
                    pass_dict[key] = pass_lst

    if len(pass_dict) == 0:
        return "All field formats are ok"
    else:
        return "There are some errors in the field format", pass_dict


def datatype_match(file1, file2):
    config_df = file2
    extract = file1

    config_df = config_df.loc[0::, ['Field Name', 'Data Type']]
    config_df = config_df.dropna()
    dict_df = config_df.set_index('Field Name')['Data Type'].to_dict()
    #dict_df.pop("SHIP_DATE")
    extract["REFERRAL_DATE"] = extract["REFERRAL_DATE"].astype('Int64')
    extract["PATIENT_CONSENT_DATE"] = extract["PATIENT_CONSENT_DATE"].astype('Int64')

    pass_dict = dict()
    for key in dict_df.keys():
        dict_df[key] = re.sub("\(.*?\)", "", dict_df[key])

    def datatype_validate(pattern, test_str):

        if pattern == "DATE":
            format = "%Y%m%d"
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

        elif pattern == "VARCHAR":
            if isinstance(test_str, str) or isinstance(test_str, int):
                return True
            else:
                return str(test_str)

        elif pattern == "NUMERIC":
            if isinstance(test_str, float):
                return True
            else:
                return str(test_str)

        elif pattern == "INTEGER":
            if isinstance(test_str, int):
                return True
            else:
                return str(test_str)

    for key in dict_df.keys():
        pass_lst = []
        if key not in extract.columns:
            continue
        else:
            for row in extract[key]:
                if pd.isnull(row):
                    continue
                else:
                    format = dict_df[key]
                    x = datatype_validate(format, str(row))
                    if x != True:
                      pass_lst.append(x)

        if len(pass_lst)!=0:
          pass_dict[key] = pass_lst

    # i = False
    # if i in pass_lst:
    #     return False
    # else:
    #     return True
    if len(pass_dict)==0:
      return "All data types are matched"
    else:
      return "There is some error with the data type of these values: ", pass_dict


def expected_values_match(file1, file2):
    config_df = file2
    extract = file1
    config_df = config_df.loc[0::, ['Field Name', 'Expected Value/s (comma separated)']]
    config_df = config_df.dropna()
    dict_df = config_df.set_index('Field Name')['Expected Value/s (comma separated)'].to_dict()
    pass_dict = dict()

    for key in dict_df.keys():
        pass_lst = []
        if key not in extract.columns:
            continue
        else:
            for row in extract[key]:

                if pd.isnull(row):
                    continue
                elif row in dict_df[key]:
                    pass
                    # pass_lst.append(True)
                else:
                    pass_lst.append(row)

        if len(pass_lst) != 0:
            pass_dict[key] = pass_lst

    if len(pass_dict) == 0:
        return "All expected values are matched"
    else:
        return "There is some error with the expected values of these values: ", pass_dict
