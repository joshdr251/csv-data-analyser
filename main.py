
import pandas as pd
import sys

def main():
    """
    Control of various functions. Serves as the control center.

    :raises AttributeError: If the specified function cannot be found.
    :raises TypeError: If the parameters provided do not match the target function's signature.
    :raises ValueError: If user_intended_function is not between 1 and 8.
    """

    filepath, delimiter = user_input_filepath_delimiter()
    data = load_file(filepath, delimiter)

    while True:
        try:
            user_intended_function = int(input("\n==========================================="
                                               "\n1. View CSV File (preview of raw data)\n"
                                               "2. Display Basic Information (Metadata)\n"
                                               "3. Data Cleaning Options\n"
                                               "4. Numerical Analysis (if numbers detected)\n"
                                               "5. Categorical Analysis\n"
                                               "6. Export Cleaned Data\n"
                                               "7. Create Graphic (via Matplotlib/Seaborn)\n"
                                               "8. Exit\n"
                                               # auch Datei speichern
                                               "-- Press number to continue: "))
            print("===========================================")

            if not (1 <= user_intended_function <= 8):
                raise ValueError("RangeError")

        except ValueError as value_error:
            if str(value_error) == "RangeError":
                print("\nError: Input has to be between 1 and 8")
            else:
                print("\nError: Is String, has to be INTEGER")
        except TypeError:
            print("\nError: Incompatible data type")

        else:
            if user_intended_function == 1:
                print_data(data)
            elif user_intended_function == 2:
                get_metadata(data)
            elif user_intended_function == 3:
                data = clean_data(data)
            elif user_intended_function == 8:
                terminate_program()


def user_input_filepath_delimiter():
    """
    Take filepath and delimiter from user and return for further usage.

    :returns: The filepath and the delimiter  entered by the user.
    :raises FileNotFoundError: If the file at the given path is not found.
    :raises pd.errors.EmptyDataError: If the file is empty.
    :raises pd.errors.ParserError: If the file contains an invalid delimiter.
    """

    while True:
        filepath_user_input = str(input("======== CSV Data Analyser ========"
                                        "\nInsert filepath: "))
        delimiter = input("Separator(, or ; or \\t or |): ")
        delimiter = delimiter.replace("\\t", "\t")

        try:
            data = pd.read_csv(filepath_user_input, sep=delimiter, encoding="utf-8")

            # checking separator
            if len(data.columns) == 1:
                confirm_single_column = input("Just one column detected (y/n): ")
                if confirm_single_column == "y":
                    pass
                elif confirm_single_column == "n" and delimiter not in data.columns[0]:
                    print("Separator seems to not be valid")
                    continue
                else:
                    print("Enter y or n")
                    continue

        except FileNotFoundError:
            print("\nError: File not existing\n")
            continue
        except pd.errors.EmptyDataError:
            print("\nError: File is empty\n")
            continue
        except pd.errors.ParserError:
            print("\nError: Separator not valid\n")
            continue

        return filepath_user_input, delimiter


def load_file(filepath, delimiter):
    """
    Read the selected file and return its content.

    :param filepath: The filepath of the file to be read.
    :param delimiter: The delimiter used in the CSV file.
    :returns: The content of the selected file as a DataFrame.
    """

    data = pd.read_csv(filepath, sep=delimiter, skipinitialspace=True, encoding="utf-8")
    data.columns = data.columns.str.strip()
    return data


def print_data(data):
    """
    Print the content of the selected file.

    :param data: The content of the file that has been read.
    :raises ValueError: If load_file returns 'None'.
    """

    if data is None:
        return
    print("\n---- Preview of raw data ----\n" + data.head().to_string(index=False))


def get_metadata(data):
    """
    Determine the metadata of the selected file.

    :param data: The content of the file that has been read.

    - Speicherplatzverbrauch
    """

    if data is None:
        return

    print("\n---- Metadata ----")
    print("\n-- Number of rows and columns:")

    # rows and ex NaN
    count_all_rows = len(data)
    count_rows_ex_nan = len(data.dropna())
    print(f"All rows: {count_all_rows}; ex NaN: {count_rows_ex_nan}")


    # columns and ex NaN
    count_all_columns = len(data.columns)
    count_columns_ex_nan = data.dropna(axis=1).shape[1]
    print(f"All columns: {count_all_columns}; and ex NaN: {count_columns_ex_nan}")

    type_mapping = {
        "str": "string",
        "object": "string",
        "int64": "integer",
        "float64": "float",
        "bool": "boolean",
        "datetime64[ns]": "datetime"
    }

    data_types = data.dtypes.to_dict()

    key_list = []
    correct_value_list = []
    for key, value in data_types.items():
         key_str = str(key)
         key_list.append(key_str)

         value_str = str(value)
         correct_value = type_mapping.get(value_str, "unknown")
         correct_value_list.append(correct_value)

    print("\n-- Data types sorted by column name:")

    for field_name, field_data_type in zip(key_list, correct_value_list):
        print(f"{field_name}: {field_data_type}")


def clean_data(data):

    ### Wie überarbeitete Version an Nutzer zurückgeben? In gesamtem Code schauen ###

    while True:
        try:
            clean_options = int(input("\n1. Drop missing values\n"
                                  "2. Fill missing values\n"
                                  "3. Remove duplicates\n"
                                  "4. Strip whitespaces\n"
                                  "5. Fix data types\n"
                                  "6. Exit\n"
                                  "-- Press number to continue: "))

            if not (1 <= clean_options <= 6):
                raise ValueError("RangeError")

        except ValueError as value_error:
            if str(value_error) == "RangeError":
                print("\nError: Input has to be between 1 and 6")
            else:
                print("\nError: Is String, has to be INTEGER")
        except TypeError:
            print("\nError: Incompatible data type")

        else:
            if clean_options == 1:
                data = data.dropna()
                print(data.to_string(index=False))
            elif clean_options == 2:
                for column in data.columns:
                    converted = pd.Series(pd.to_numeric(data[column], errors="coerce"))
                    if converted.notna().sum() > (len(data) * 0.5):
                        data[column] = converted

                text_columns = data.select_dtypes(include=["object", "category", "str"]).columns
                if not text_columns.empty:
                    data[text_columns] = data[text_columns].fillna("Unknown")

                num_columns = data.select_dtypes(include=["number"]).columns

                if not num_columns.empty:
                    for column in num_columns:
                        median_value = data[column].median()

                        if pd.isna(median_value):  # if column contains only NaN
                            median_value = 0

                        data[column] = data[column].fillna(median_value)

                print(data.to_string(index=False))
            elif clean_options == 3:
                data = data.drop_duplicates()
                print(data.to_string(index=False))
            elif clean_options == 4:
                data = data.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
                print(data.to_string(index=False))
            elif clean_options == 5:
                    while True:

                        print("\nAvailable columns:")
                        data_columns_list = list(data.columns)
                        for index, column in enumerate(data_columns_list, start=1):
                            preview = ", ".join(data[column].head(3).astype(str))
                            print(f"{index}. ‒ '{column}' ‒ current type:  {data[column].dtype} ‒ brief preview: [{preview}]")

                        print(f"{len(data_columns_list) + 1}. Exit")

                        try:
                            column_choice = int(input("\n-- Press number to continue: "))
                            if not (1 <= column_choice <= len(data_columns_list) + 1):
                                raise ValueError("RangeError")
                        except ValueError as value_error:
                            if str(value_error) == "RangeError":
                                print(f"\nError: Input has to be between 1 and {len(data_columns_list) + 1}")
                            else:
                                print(f"\nError: Input a number")
                            continue

                        if column_choice == len(data_columns_list) + 1:
                            break

                        selected_column = data_columns_list[column_choice - 1]

                        try:
                            target_dtype = int(input("\nConvert to:\n"
                                                     "1. Integer\n"
                                                     "2. Float\n"
                                                     "3. Datetime\n"
                                                     "4. Boolean\n"
                                                     "5. Category\n"
                                                     "6. Skip\n"
                                                     "-- Press number to continue: "))

                            if not (1 <= target_dtype <= 6):
                                raise ValueError("RangeError")
                        except ValueError as value_error:
                            if str(value_error) == "RangeError":
                                print("\nError: Input has to be between 1 and 6")
                            else:
                                print("\nError: Input a number")
                            continue

                        else:
                            if target_dtype == 6:
                                continue

                            try:
                                if target_dtype == 1:
                                    data[selected_column] = pd.to_numeric(data[selected_column], errors="coerce").astype("Int64")
                                elif target_dtype == 2:
                                    data[selected_column] = pd.to_numeric(data[selected_column], errors="coerce")
                                elif target_dtype == 3:
                                    data[selected_column] = pd.to_datetime(data[selected_column], errors="coerce")
                                elif target_dtype == 4:
                                    bool_map = {"true": True, "false": False, "yes": True, "no": False, "1": True, "0": False}
                                    data[selected_column] = data[selected_column].astype(str).str.lower().map(bool_map)
                                    if data[selected_column].isna().any():
                                        print("Warning: some values could not be mapped and are now NaN")
                                elif target_dtype == 5:
                                    data[selected_column] = data[selected_column].astype("category")

                                print(f"\n[Success] column '{selected_column}' has been successfully converted to {data[selected_column].dtype}")

                            except Exception as error:
                                print(f"\nError during conversion: {error}")

            elif clean_options == 6:
                print("Clean mode terminated. Data has been updated.")
                break

    return data  # return updated content


def terminate_program():
    print("\nProgram has been manually terminated...")
    sys.exit()


main()