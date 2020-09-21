def extract_clauses(string):
    print(f"String:\n {string}\n")
    if 'where' in string:
        split_keyword = 'where'
    else:
        split_keyword = 'group by'

    stack = []
    current_word = ''
    split_position = -1
    for i, char in enumerate(string):
        print(f"'{char}'", current_word)
        if char in [' ', '\t', '\n']:
            if current_word == split_keyword:
                print(stack)
                while stack[-1] != 'select':
                    stack.pop()
                stack.pop()
                if len(stack) == 0:
                    split_position = i
                    break
            if char == ' ' and current_word == 'group':
                current_word = current_word + char
            else:
                current_word = ''
            # else:
            #     current_word = current_word + char
        else:
            current_word = current_word + char
        if current_word in ['select', 'from']:
            stack.append(current_word)

    # print(string.split(split_keyword))
    # select_from = string.split(split_keyword)[0]
    select_from = string[:split_position - len(split_keyword)]
    # print("select_from", select_from)
    # conditions_clause = split_keyword.join(string.split(split_keyword)[1:])
    conditions_clause = string[split_position:]
    # print("where_clause", where_clause)
    from_clause = 'from'.join(select_from.split('from')[1:])
    select_clause = select_from.split('from')[0]
    from_clause = from_clause.strip()
    return select_from, conditions_clause, select_clause, from_clause, split_keyword


def create_filtered_queries(args, input_path, table_column_dict):
    with open(input_path, 'r') as f:
        string = f.read()
        # print(string)
        query_options = string.split('go')[0]
        # print(string.split('\ngo\n'))
        string = '\ngo\n'.join(
            list(filter(lambda x: len(x.strip()) > 0, string.split('\ngo\n')))[-1:])
        select_from, where_clause, select_clause, from_clause, split_keyword = extract_clauses(
            string)
        # print(f"From Clause: \n{from_clause}")
        if from_clause[0] == '(':
            inner_statement = from_clause[1:-1]
            count = 0
            stack = []
            for char in from_clause:
                if char == '(':
                    stack.append(char)
                elif char == ')':
                    stack.pop()
                    if len(stack) == 0:
                        break
                count += 1
            inner_statement = from_clause[1:count]
            print(f"Inner Statement:\n{inner_statement}")
            inner_select_from, inner_where, _, inner_from, _ = extract_clauses(
                inner_statement)
            if ',' in inner_from:
                tables = inner_from.strip().split(',')
            else:
                tables = inner_from.strip().split('left outer join')
            for table in tables:
                table = table.strip()
                for column, column_data_type in table_column_dict[table]:
                    if column_data_type == "int":
                        extra_filter_1 = f"{column} > {1000}"
                        extra_filter_2 = f"{column} < {10}"
                        from_clause_1 = f"{inner_select_from} where {extra_filter_1} and {inner_where}"
                        from_clause_2 = f"{inner_select_from} where {extra_filter_2} and {inner_where}"
                        filtered_query_1 = f"{query_options}\ngo\n{select_clause} from ({from_clause_1}) {split_keyword} {extra_filter_1} and {where_clause}"
                        filtered_query_2 = f"{query_options}\ngo\n{select_clause} from ({from_clause_2})  {split_keyword}where {extra_filter_2} and {where_clause}"
                        return filtered_query_1, filtered_query_2
        tables = from_clause.split(',')
        for table in tables:
            table = table.strip()
            for column, column_data_type in table_column_dict[table]:
                if column_data_type == "int":
                    extra_filter_1 = f"{column} > {1000}"
                    extra_filter_2 = f"{column} < {10}"
                    filtered_query_1 = f"{query_options}\ngo\n{select_from} where {extra_filter_1} and {where_clause}"
                    filtered_query_2 = f"{query_options}\ngo\n{select_from} where {extra_filter_2} and {where_clause}"
                    return filtered_query_1, filtered_query_2


def extract_table_text(string, dataset):
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
        if dataset == "tpch":
            separator = ","
        elif dataset == "tpcds":
            separator = "\n"
        for column_string in table_content.split(separator):
            if len(column_string) == 0:
                continue
            if column_string[-1] == ",":
                column_string = column_string[:-1]
            column_strings = column_string.strip()
            if column_strings.find("PRIMARY KEY") == 0:
                break
            column_strings = column_strings.split()
            print(column_strings)
            column_name = column_strings[0]
            column_data_type = column_strings[1]
            table_column_dict[table_header].append(
                (column_name, column_data_type))
    for k, v in table_column_dict.items():
        print(k)
        for column in v:
            print(column)
    return table_column_dict


def extract_tables_columns(schema_path, dataset="tpch"):
    # get the string for each table
    if dataset in ("imdbload", "tpcds"):
        with open(schema_path) as f:
            string = f.read()
            table_column_dict = extract_table_text(string, dataset)
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
    print(extract_tables_columns(
        "../schema/imdbload-postgres.sql", "imdbload").keys())
