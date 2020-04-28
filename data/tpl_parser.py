import re
from data.dropdown_control import Dropdown_Control

# Read file
# Capture data: assign, ignore [comments, if statements], includes


sample = """{include file="global/widgets/dynamic_mapping/single_multiselection_tier_dropdown_widget.tpl"
    filename=$filename
    options=$dropdown_options
}
"""


def get_widget_type(include_section):
    widget_type = re.compile(
        r'file="global/widgets/dynamic_mapping/(.*?).tpl')
    match = widget_type.search(include_section)
    if not match:
        raise Exception("Widget type not found")
    return match[1]


def get_include_variable(include_section):
    include_list = re.split(r'\s+', include_section)[1:]
    include_list = list(map(lambda x: x.replace("$", ""), include_list))

    param_dict = {}
    for param in include_list:
        param_list = param.split('=')
        param_dict[param_list[0]] = param_list[1]
    return param_dict


def get_assign_vars(section):
    assign_pattern = re.compile(
        r'\{assign var=[\'"](.*)[\'"] value=[\'"](.*?)[\'"]\}')
    matches = assign_pattern.findall(section)
    if matches:
        return matches
    return []


def get_assign_array_vars(section):
    assign_pattern = re.compile(
        r'\{assign_array var_name=[\'"]*(.*?)[\'"]*\n(.*?)\}', re.DOTALL)
    matches = assign_pattern.findall(section)
    cleaned_matches = []
    if matches:
        for match in matches:
            cleaned_arg_list = re.split(r'\n\s*', match[1].strip())
            cleaned_tuple = (match[0], cleaned_arg_list)
            cleaned_matches.append(cleaned_tuple)
    return cleaned_matches


def get_tuple(data):
    key, value = data.split("=")
    value = value.strip('\'"')
    return (key, value)


def get_dropdown_objects(data_dict):
    dropdown_objs = []

    for idx, option in enumerate(data_dict['options']):
        new_dropdown = {}
        name, required = option
        new_dropdown['name'] = name
        new_dropdown['filename'] = data_dict['filename']
        if required:
            new_dropdown['required'] = True
        if 'labels' in data_dict:
            label = data_dict['labels'][idx][1]
        else:
            label = name
        new_dropdown['label'] = label
        if 'default' in data_dict:
            new_dropdown["defaults"] = [data_dict['default'][idx][1]]
        new_dropdown['parents'] = [option[0]
                                   for option in data_dict['options'][:idx]]
        new_dropdown['children'] = [option[0]
                                    for option in data_dict['options'][idx + 1:]]
        dropdown_objs.append(new_dropdown)
    return dropdown_objs


with open("tests/sampler.tpl") as tpl_obj:
    contents = tpl_obj.read().strip()
    include_pattern = re.compile(
        r'^\s*\{include(.*?)\}', re.DOTALL | re.MULTILINE)
    include_sections = re.findall(include_pattern, contents)
    data_sections = re.split(include_pattern, contents)
    data_sections = [x.strip() for x in data_sections[::2] if x]
    for idx, match in enumerate(include_sections):
        match = match.strip()
        widget_type = get_widget_type(match)
        var_data_dict = get_include_variable(match)
        var_assigns = get_assign_vars(data_sections[idx])
        assign_arrays = get_assign_array_vars(data_sections[idx])
        assign_arrays.extend(var_assigns)
        name_value_dict = {}
        for pair in assign_arrays:
            name_value_dict[pair[0]] = pair[1]
        for key, value in var_data_dict.items():
            try:
                var_data_dict[key] = name_value_dict[var_data_dict[key]]
            except KeyError:
                print(f'Missing {key} key in variable dict')

        # Map lists of strings intu tuples (key, value)
        for key, value in var_data_dict.items():
            if type(value) == list:
                var_data_dict[key] = list(map(get_tuple, value))

        controls = []
        if widget_type == 'multi_tier_dropdown_widget':
            dropdowns = get_dropdown_objects(var_data_dict)
            dropdown_objs = list(
                map(lambda x: Dropdown_Control(**x), dropdowns))
            for dropdown in dropdown_objs:
                print(dropdown)
        # print(assigns)
        # print(assign_arrays)
        # for key, value in var_data_dict:

        # Get all includes
        # Get all arg vars
        # Inject arg vars into include dict
