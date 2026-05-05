
import pandas as pd

def main():
    """
    Control of various functions. Serves as the control center.

    :raises AttributeError: If the specified function cannot be found.
    :raises TypeError: If the parameters provided do not match the target function's signature.
    :raises ValueError: If user_intended_function is not between 1 and 8.
    """

    filepath, delimiter = user_input_filepath_delimiter()

    while True:
        try:
            user_intended_function = int(input("\n==========================================="
                                               "\n1. View CSV File (preview of raw data)\n"
                                           "2. Display Basic Information (Metadata)\n"
                                           "3. Data Cleaning Options\n"
                                           "4. Numerical Analysis (if numbers detected)\n"
                                           "5. Categorial Analysis\n"
                                           "6. Export Cleaned Data\n"
                                           "7. Create Graphic (via Matplotlib/Seaborn)\n"
                                           "8. Exit\n"
                                           "-- Press number to continue: "))
            print("===========================================")

            if not (1 <= user_intended_function <= 8):
                raise ValueError("RangeError")

        except ValueError as value_error:
            if str(value_error) == "RangeError":
                print("\nFehler: Muss zwischen 1 und 8 sein")
            else:
                print("\nFehler: Ist String, muss INTEGER sein")
        except TypeError:
            print("\nFehler: Inkompatibler Datentyp")

        else:
            if user_intended_function == 1:
                print_data(filepath, delimiter)
            elif user_intended_function == 2:
                get_metadata(filepath, delimiter)


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
            print("\nFile not existing\n")
            continue
        except pd.errors.EmptyDataError:
            print("\nFile is empty\n")
            continue
        except pd.errors.ParserError:
            print("\nSeparator not valid\n")
            continue

        return filepath_user_input, delimiter


def load_file(filepath, delimiter):
    """
    Read the selected file and return its content.

    :param filepath: The filepath of the file to be read.
    :param delimiter: The delimiter used in the CSV file.
    :returns: The content of the selected file as a DataFrame.
    """

    data = pd.read_csv(filepath, sep=delimiter, encoding="utf-8")
    return data


def print_data(filepath, delimiter):
    """
    Print the content of the selected file.

    :param filepath: The filepath of the file to be read.
    :param delimiter: The delimiter used in the CSV file.
    :raises ValueError: If load_file returns 'None'.
    """

    data = load_file(filepath, delimiter)
    if data is None:
        return
    print("\n---- Preview of raw data ----\n" + data.head().to_string(index=False))


def get_metadata(filepath, delimiter):
    """
    Determine the metadata of the selected file.

    :param filepath: The filepath of the file to be read.
    :param delimiter: The delimiter used in the CSV file.

    - Speicherplatzverbrauch
    """

    data = load_file(filepath, delimiter)
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

    print("\n--Data types sorted by column name:")

    for field_name, field_data_type in zip(key_list, correct_value_list):
        print(f"{field_name}: {field_data_type}")


main()