
def extract_tables_columns(schema_path):
    # get the string for each table
    table_column_dict = {}
    with open(schema_path, "r") as f:
        string = f.read()
        string = list(string.split("GO"))
        table_strings = string[2:-1]
        for table_string in table_strings:
            start, end = table_string.find('('), table_string.rfind(')')
            table_content = table_string[start + 1: end]
            table_header = table_string[:start]
            table_name = table_header[table_header.rfind(
                '[') + 1: table_header.rfind(']')]
            print(f"Table name: {table_name}")
            table_column_dict[table_name] = []
            column_strs = list(table_content.split(','))
            for column_str in column_strs:
                if '[' not in column_str or ']' not in column_str:
                    continue
                column_name = column_str[column_str.find(
                    '[') + 1: column_str.find(']')]
                column_data_type = column_str[column_str.rfind('[') + 1: column_str.rfind(']')]
                column_name = column_name.lower()
                table_column_dict[table_name].append((column_name, column_data_type))
                print(column_name, column_data_type)
    return table_column_dict

if __name__ == "__main__":
    extract_tables_columns("../tpc-h.sql")