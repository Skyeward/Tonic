from typing import Iterable

#┌─┄┐├┤└┼┘╭╮╰╯┆│ ┬┴

def indexed_menu(columns: {str: Iterable[str]}, title: str = "", show_column_headers: bool = False) -> [str]:
    "Prints a generic table with numeric options. Keys in the 'columns' dictionary are column headers (these must be enabled with show_column_headers)."
    
    FRAME = {"vert": "│", "horiz": "─", "tl_corner": "┌", "tr_corner": "┐", "bl_corner": "└", "br_corner": "┘", "left_junc": "├", "right_junc": "┤", "top_junc": "┬", "mid_junc": "┼", "bottom_junc": "┴"}
    
    return_table = []
    
    table_top_line = ""
    table_title = ""
    table_separator_title_headers = ""
    table_column_headers = ""
    table_separator_headers_body = ""
    table_body = []
    table_bottom_line = ""
    
    max_column_widths = []
    max_column_length = 0
    table_width = 0

    #FINDING MAX VALUES FOR EACH COLUMN WIDTH (USED FOR PADDING) AND MAX COLUMN LENGTH
    for column_number, column_data in enumerate(columns.items()):
        column_header = column_data[0]
        column_entries = column_data[1]
        max_column_length = max(max_column_length, len(column_entries))

        if show_column_headers == True:
            max_column_widths.append(len(column_header))
        else:
            max_column_widths.append(0)

        for i, column_entry in enumerate(column_entries):
            if column_entry == None:
                columns[column_header][i] = ""
                column_entry = ""

            current_max_width = max_column_widths[column_number]
            width_to_compare = len(column_entry)
            max_column_widths[column_number] = max(current_max_width, width_to_compare)

    largest_index = max_column_length - 1
    max_index_column_width = len(str(largest_index))
    
    #GENERATING TABLE BODY; ALSO FINDS MAXIMUM TABLE ROW WIDTH
    for row_number in range(max_column_length):
        index_as_string = str(row_number)
        index_padding_length = max_index_column_width - len(index_as_string)
        index_padding = " " * index_padding_length
        table_body_new_row = f"{FRAME['vert']} {index_as_string} {index_padding}"

        for i, column in enumerate(columns.values()):
            try:
                item_text = column[row_number]
            except:
                item_text = ""

            column_padding_length = max_column_widths[i] - len(item_text)
            column_padding = " " * column_padding_length
            table_body_new_row += f"{FRAME['vert']} {item_text} {column_padding}"

        table_body_new_row += FRAME["vert"]
        table_width = max(table_width, len(table_body_new_row))
        table_body.append(table_body_new_row)

    #GENERATING TABLE TOP LINE, TITLE LINE AND HEADERS LINE
    table_width_without_edges = table_width - 2
    horizontal_section = FRAME["horiz"] * table_width_without_edges
    table_top_line = f"{FRAME['tl_corner']}{horizontal_section}{FRAME['tr_corner']}"
    title_with_edge_padding = f" {title} "
    centred_title = _centre_align_string(table_width_without_edges, title_with_edge_padding)
    table_title = f"{FRAME['vert']}{centred_title}{FRAME['vert']}"
    padding_above_indexes = " " * (max_index_column_width + 2)
    line_above_indexes = padding_above_indexes.replace(" ", FRAME["horiz"])

    headers_section = padding_above_indexes

    for column_number, column_header in enumerate(columns.keys()):
        column_width = max_column_widths[column_number]
        headers_section += f"{FRAME['vert']} {_centre_align_string(column_width, column_header)} "

    table_column_headers = f"{FRAME['vert']}{headers_section}{FRAME['vert']}"

    #GENERATING SEPARATORS AND BOTTOM LINE
    if show_column_headers == True:
        space_above_indexes = padding_above_indexes
        left_edge_character = FRAME["vert"]
    else:
        space_above_indexes = line_above_indexes
        left_edge_character = FRAME["left_junc"]

    table_separator_title_headers = f"{left_edge_character}{space_above_indexes}"
    table_separator_headers_body = f"{FRAME['left_junc']}{line_above_indexes}"
    table_bottom_line = f"{FRAME['bl_corner']}{line_above_indexes}"

    for column_number, column_header in enumerate(columns.keys()):
        if column_number != 0 or show_column_headers == False:
            junc_type = "top_junc"
        else:
            junc_type = "tl_corner"

        column_line_width = max_column_widths[column_number] + 2
        table_separator_title_headers += f"{FRAME[junc_type]}{FRAME['horiz'] * column_line_width}"
        table_separator_headers_body += f"{FRAME['mid_junc']}{FRAME['horiz'] * column_line_width}"
        table_bottom_line += f"{FRAME['bottom_junc']}{FRAME['horiz'] * column_line_width}"

    table_separator_title_headers += FRAME["right_junc"]
    table_separator_headers_body += FRAME["right_junc"]
    table_bottom_line += FRAME["br_corner"]

    #BUILDING TABLE TO RETURN
    return_table.append(table_top_line)
    return_table.append(table_title)
    return_table.append(table_separator_title_headers)

    if show_column_headers == True:
        return_table.append(table_column_headers)
        return_table.append(table_separator_headers_body)

    for row in table_body:
        return_table.append(row)

    return_table.append(table_bottom_line)

    #IF TITLE IS WIDER THAN TABLE, ADDS PADDING TO RIGHT EDGE OF LAST COLUMN
    title_overhang = len(table_title) - len(table_top_line)
    
    if title_overhang > 0:
        title_row_to_skip = 1
        length_to_add = title_overhang

        for row_number, row in enumerate(return_table):
            if row_number == title_row_to_skip:
                continue
            
            row_end_character = row[-1]
            row_pad_character = row[-2]
            row_without_right_edge = row[:-1]
            row_extended = f"{row_without_right_edge}{row_pad_character * length_to_add}{row_end_character}"
            return_table[row_number] = row_extended

    return return_table


def _centre_align_string(row_width, text):
    padding_length_total = row_width - len(text)
    padding = " " * padding_length_total
    padding_length_half = int(padding_length_total / 2)
    padding_left = padding[:padding_length_half]
    padding_right = padding[padding_length_half:]

    text_with_padding = f"{padding_left}{text}{padding_right}"
    return text_with_padding


def format_string(string_to_format: str, make_lowercase: bool = True, remove_special_characters: bool = True, char_replacements: {str: str} = None):
    "Formats a string based on chosen rules. char_replacements will replace the any appearances of keys with their associated value."

    formatted_input = string_to_format
    
    if char_replacements != None:
        for char_to_replace, replacement_char in char_replacements.items():
            if char_to_replace == replacement_char:
                continue

            formatted_input = formatted_input.replace(char_to_replace, replacement_char)
    
    formatted_input = formatted_input.strip()

    while formatted_input.find("  ") != -1: #removes any spacing larger than a single space
        formatted_input = formatted_input.replace("  ", " ")

    if remove_special_characters == True:
        formatted_input = "".join(char for char in formatted_input if ord(char) > 31 and ord(char) < 126)

    if make_lowercase == True:
        formatted_input = formatted_input.lower()
    
    return formatted_input


def get_instance_variables(instances: [type], variable_name: str):
    "Returns a list of values for a given variable name in a list of class instances."

    return_list = []
    
    for instance in instances:
        return_list.append(vars(instance)[variable_name])

    return return_list


def get_valid_index(number_of_options: int, fail_message: [str] = None, input_indicator: str = ">>> ") -> int:
    "Continues to take user inputs until the user types an integer between zero (inclusive) and number_of_options (exclusive)."
    
    if number_of_options < 1:
        raise ValueError("number of options must be an integer greater than zero")
    
    user_input = format_string(input(input_indicator), False, True)

    try:
        user_input = int(user_input)
    except:
        user_input = -1

    if 0 <= user_input < number_of_options:
        return user_input
    else:
        if fail_message != None:
            print(fail_message)
        
        return get_valid_index(number_of_options, fail_message, input_indicator)


def get_unique_string(unavailable_strings: [str], input_message: str, fail_message: str, cancel_strings: [str] = ["", "cancel"]) -> str:
    "Continually asks for string from user until a string is given not in unavailable_strings. Can optionally be given a list of strings which cancel the funtion (use lowercase). Returns the new name, or None if cancelled by user."
    
    input_is_unique = False
        
    if cancel_strings == None:
        cancel_strings = []

    if unavailable_strings == None:
        unavailable_strings = []

    if input_message == None:
        input_message = ""
    
    if fail_message == None:   
        fail_message = ""

    print(input_message)

    while input_is_unique == False:
        user_input = format_string(input(">>> "))

        if user_input in cancel_strings:
            return None

        if user_input in unavailable_strings:
            print(fail_message)
        else:
            input_is_unique = True

    return user_input