
import pandas as pd
import sys

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import seaborn as sns

import tkinter as tk
from tkinter import filedialog


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
                                               "\n1. View CSV file (preview of raw data)\n"
                                               "2. Display basic information (Metadata)\n"
                                               "3. Data cleaning options\n"
                                               "4. Numerical analysis (if numbers detected)\n"
                                               "5. Categorical analysis\n"
                                               "6. Create graphic (via Matplotlib/Seaborn)\n"
                                               "7. Save cleaned data\n"
                                               "8. Exit\n"
                                               "-- Press number to continue: "))
            print("===========================================")

            if not (1 <= user_intended_function <= 8):
                raise ValueError("RangeError")

        except ValueError as value_error:
            if str(value_error) == "RangeError":
                print("\n[Error]: Input has to be between 1 and 8")
            else:
                print("\n[Error]: Is String, has to be INTEGER")
        except TypeError:
            print("\n[Error]: Incompatible data type")

        else:
            if user_intended_function == 1:
                print_data(data)
            elif user_intended_function == 2:
                get_metadata(data)
            elif user_intended_function == 3:
                data = clean_data(data)
            elif user_intended_function == 4:
                get_numerical_analysis(data)
            elif user_intended_function == 5:
                get_categorical_analysis(data)
            elif user_intended_function == 6:
                create_graphic(data)
            elif user_intended_function == 7:
                save_cleaned_data(data)
            elif user_intended_function == 8:
                terminate_program()


def user_input_filepath_delimiter():
    """
    Take filepath and delimiter from user and return for further usage.

    :returns: The filepath and the delimiter entered by the user.
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
                confirm_single_column = input("[Info] Just one column detected (y/n): ")
                if confirm_single_column == "y":
                    pass
                elif confirm_single_column == "n" and delimiter not in data.columns[0]:
                    print("[Error]: Separator seems to not be valid\n")
                    continue
                else:
                    print("Enter y or n")
                    continue

        except FileNotFoundError:
            print("\n[Error]: File not existing\n")
            continue
        except pd.errors.EmptyDataError:
            print("\n[Error]: File is empty\n")
            continue
        except pd.errors.ParserError:
            print("\n[Error]: Separator not valid\n")
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
    """
    Clean the given data by different aspects and return for further usage.

    :param data: The data to be cleaned.
    :returns: The data that has been cleaned.
    """

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
                print("\n[Error]: Input has to be between 1 and 6")
            else:
                print("\n[Error]: Is String, has to be INTEGER")
        except TypeError:
            print("\n[Error]: Incompatible data type")

        else:
            if clean_options == 1:
                data = data.dropna()
                print(f"\n[Success] Dropped rows with missing values. Rows remaining: {len(data)}")
            elif clean_options == 2:
                data = _fill_missing_values(data)
                print(f"\n[Success] Missing values filled.")
            elif clean_options == 3:
                data = data.drop_duplicates()
                print(f"\n[Success] Duplicates removed. Rows remaining: {len(data)}")
            elif clean_options == 4:
                data = data.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
                print(f"\n[Success] Whitespaces stripped.")
            elif clean_options == 5:
                data = _fix_data_types(data)
            elif clean_options == 6:
                print("[Info] Clean mode terminated. Data has been updated.")
                break

    return data


def _fill_missing_values(data):
    """
    Support function for filling missing values.

    :param data: The data to be filled.
    :returns: The data that has been filled.
    """

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

    return data


def _fix_data_types(data):
    """
    Support function for fixing data types.

    :param data: The data to be fixed.
    :returns: The data that has been fixed.
    :raises ValueError: If the input is wrong.
    :raises Exception: If the column conversion fails due to an incompatible value.
    """

    while True:
        print("\nAvailable columns:")
        data_columns_list = list(data.columns)
        for index, column in enumerate(data_columns_list, start=1):
            preview_list = [str(x) for x in data[column].head(3).tolist()]
            preview = ", ".join(preview_list)
            print(f"{index}. ‒ '{column}' ‒ current type:  {data[column].dtype} ‒ brief preview: [{preview}]")

        print(f"{len(data_columns_list) + 1}. Exit")

        try:
            column_choice = int(input("\n-- Press number to continue: "))
            if not (1 <= column_choice <= len(data_columns_list) + 1):
                raise ValueError("RangeError")
        except ValueError as value_error:
            if str(value_error) == "RangeError":
                print(f"\n[Error]: Input has to be between 1 and {len(data_columns_list) + 1}")
            else:
                print(f"\n[Error]: Input a number")
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
                print("\n[Error]: Input has to be between 1 and 6")
            else:
                print("\n[Error]: Input a number")
            continue

        else:
            if target_dtype == 6:
                continue

            try:
                col_backup = data[selected_column].copy()

                if target_dtype == 1:
                    col_backup = pd.to_numeric(col_backup, errors="coerce").astype("Int64")
                elif target_dtype == 2:
                    col_backup = pd.to_numeric(col_backup, errors="coerce")
                elif target_dtype == 3:
                    col_backup = pd.to_datetime(col_backup, errors="coerce")
                elif target_dtype == 4:
                    bool_map = {"true": True, "false": False, "yes": True, "no": False, "1": True, "0": False}
                    col_backup = col_backup.astype(str).str.lower().map(bool_map)
                    if col_backup.isna().any() and not data[selected_column].isna().any():
                        print("[Warning]: some values could not be mapped and are now NaN")
                elif target_dtype == 5:
                    col_backup = col_backup.astype("category")

                data[selected_column] = col_backup
                print(f"\n[Success] Column '{selected_column}' has been successfully converted to {data[selected_column].dtype}")

            except Exception as error:
                print(f"\n[Error] during conversion: {error}")
                print("[Info] Column was not changed.")
                continue

    return data


def get_numerical_analysis(data):
    """
    Analyze the numerical columns.

    :param data: The data to be analyzed.
    :returns: The analysis result.
    :raises ValueError: If the input is wrong.
    """

    numerical_columns = list(data.select_dtypes(include=["int64", "Int64", "float64"]).columns)
    sum_num_columns = len(numerical_columns)

    print("")

    counter = 0
    for column in numerical_columns:
        counter += 1
        print(f"Column {counter}: {column}")

    while True:
        try:
            target_column = int(input("-- Press number to continue: "))

            if not (1 <= target_column <= sum_num_columns):
                raise ValueError("RangeError")

            break
        except ValueError as value_error:
            if str(value_error) == "RangeError":
                print(f"\n[Error]: Input has to be between 1 and {counter}")
            else:
                print("\n[Error]: Input a number")

    selected_column = numerical_columns[target_column - 1]

    sum_values = data[selected_column].sum()
    average = data[selected_column].mean()
    median = data[selected_column].median()
    mode = data[selected_column].mode()[0]
    minimum = data[selected_column].min()
    maximum = data[selected_column].max()
    standard_deviation = data[selected_column].std()
    print(f"\nSum: {sum_values}, Average: {average}, Median: {median}, Mode: {mode}")
    print(f"Minimum: {minimum}, Maximum: {maximum}, Standard deviation: {standard_deviation}")


def get_categorical_analysis(data):
    """
    Analyze the textual columns.

    :param data: The data to be analyzed.
    :returns: The analysis result.
    :raises ValueError: If the input is wrong.
    """
    textual_columns = list(data.select_dtypes(include=["object", "category", "str"]).columns)
    sum_text_columns = len(textual_columns)

    print("")

    counter = 0
    for column in textual_columns:
        counter += 1
        print(f"Column {counter}: {column}")

    while True:
        try:
            target_column = int(input("-- Press number to continue: "))

            if not (1 <= target_column <= sum_text_columns):
                raise ValueError("RangeError")

            break
        except ValueError as value_error:
            if str(value_error) == "RangeError":
                print(f"\n[Error]: Input has to be between 1 and {counter}")
            else:
                print("\n[Error]: Input a number")

    selected_column = textual_columns[target_column - 1]

    convert_low = data[selected_column].str.strip().str.lower()
    unique_values = convert_low.nunique()
    missing_values = convert_low.isna().sum()

    count_values = convert_low.value_counts()

    print(f"\nUnique values: {unique_values}")
    print(f"Missing values: {missing_values}")
    print(f"\nFrequency distribution:")
    for value, count in count_values.items():
        print(f"{value:<30} {count}")

    cardinality_ratio = unique_values / len(data)
    if cardinality_ratio <= 0.1:
        print(f"Low cardinality: {cardinality_ratio}")
        print("[Info] Relevant for understanding data!")
    elif cardinality_ratio >= 0.6:
        print(f"High cardinality: {cardinality_ratio}")
        print("[Info] No relevance...")
    else:
        print("[Info] Neither low nor high cardinality...")


def create_graphic(data):
    """
    Create graphics based on your files data.

    :param data: The data to be visualized.
    """

    numerical_columns = list(data.select_dtypes(include=["int64", "Int64", "float64"]).columns)
    categorical_columns = list(data.select_dtypes(include=["object", "category", "str"]).columns)

    print("\n1. Visualize numerical column")
    print("2. Visualize categorical column")

    choice = int(input("-- Press number to continue: "))

    sns.set_theme(style="whitegrid")

    if choice == 1:
        for i, col in enumerate(numerical_columns, 1):
            print(f"{i}. {col}")
        idx = int(input("-- Press number to continue: ")) - 1
        selected_col = numerical_columns[idx]

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        sns.histplot(data[selected_col], kde=True)
        plt.title(f"Distribution: {selected_col}")

        plt.subplot(1, 2, 2)
        sns.boxplot(y=data[selected_col])
        plt.title(f"Boxplot: {selected_col}")

        plt.tight_layout()
        manager = plt.get_current_fig_manager()

        # suppress IDE warning: TkAgg backend provides window attribute at runtime
        # noinspection PyUnresolvedReferences
        manager.window.attributes("-topmost", True)
        plt.show()

    elif choice == 2:
        for i, col in enumerate(categorical_columns, 1):
            print(f"{i}. {col}")
        idx = int(input("-- Press number to continue: ")) - 1
        selected_col = categorical_columns[idx]

        count_values = data[selected_col].str.strip().str.lower().value_counts()

        plt.figure(figsize=(10, 5))
        sns.barplot(x=count_values.index, y=count_values.values)
        plt.title(f"Frequency distribution: {selected_col}")
        plt.xlabel("Category")
        plt.ylabel("Number")
        plt.xticks(rotation=45)
        plt.tight_layout()
        manager = plt.get_current_fig_manager()

        # suppress IDE warning: TkAgg backend provides window attribute at runtime
        # noinspection PyUnresolvedReferences
        manager.window.attributes("-topmost", True)
        plt.show()


def save_cleaned_data(data):
    """
    Save cleaned data to csv file.

    :param data: The data to be saved.
    :raises Exception: If file already exists.
    """

    root = tk.Tk()
    root.withdraw()
    root.lift()
    root.attributes("-topmost", True)
    root.focus_force()

    filepath = filedialog.asksaveasfilename(title="Save cleaned data", defaultextension=".csv")

    if not filepath:
        print("\n[Info] Saving cancelled")
        return

    try:
        if filepath.endswith(".csv"):
            delimiter = input("\nSeparator (, or ; or \\t): ").replace("\\t", "\t")
            data.to_csv(filepath, sep=delimiter, index=False, encoding="utf-8")

        print(f"\n[Success] Data saved to '{filepath}'")
    except Exception as e:
        print(f"\n[Error]: {e}")


def terminate_program():
    """
    Terminate program manually.
    """

    print("\n[Info] Program has been manually terminated...")
    sys.exit()


if __name__ == "__main__":
    main()
