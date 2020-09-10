def extract_table_text(string):
    print(string.split("CREATE TABLE"))
    string = list(string.split("CREATE TABLE"))
    table_column_dict = {}
    for table_string in string:
        table_string = table_string.strip()
        if table_string == "":
            continue
        start, end = table_string.find("("), table_string.rfind(")")
        table_content = table_string[start+1:end]
        table_header = table_string[:start].strip()
        table_column_dict[table_header] = []
        print(table_header, table_content)
        for column_string in table_content.split(","):
            column_strings = column_string.strip().split()
            column_name = column_strings[0]
            column_type = column_strings[1]
            table_column_dict[table_header].append((column_name, column_type))
    return table_column_dict


def extract_tables_columns(schema_path, dataset="tpch"):
    # get the string for each table
    if dataset == "imdbload":
        with open("../schema/imdbload-postgres.sql") as f:
            string = f.read()
            table_column_dict = extract_table_text(string)
    elif dataset == "tpch":
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
                    column_data_type = column_str[column_str.rfind(
                        '[') + 1: column_str.rfind(']')]
                    column_name = column_name.lower()
                    if column_name == "skip":
                        continue
                    table_column_dict[table_name].append(
                        (column_name, column_data_type))
                    print(column_name, column_data_type)
    return table_column_dict


if __name__ == "__main__":
    print(extract_tables_columns("../schema/imdbload-postgres.sql", "imdbload").keys())
