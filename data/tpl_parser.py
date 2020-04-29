import re
from data.dropdown_control import Dropdown_Control
from data.input_control import Input_Control

# Read file
# Capture data: assign, ignore [comments, if statements], includes


sample = """{include file="global/widgets/dynamic_mapping/single_multiselection_tier_dropdown_widget.tpl"
    filename=$filename
    options=$dropdown_options
}
"""


def get_widget_type(include_section):
    widget_type = re.compile(
        r'(.*?).tpl')
    match = widget_type.search(include_section)
    if not match:
        raise Exception(f'Widget type not found in section: {include_section}')
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


def get_default_list(default_values):
    return default_values.split('|default:')


def get_dropdown_dicts(data_dict):
    dropdown_dicts = []

    for idx, option in enumerate(data_dict['options']):
        new_dropdown = {'name': option[0], 'filename': data_dict['filename']}
        required = option[1]
        if required:
            new_dropdown['required'] = True
        if 'labels' in data_dict:
            label = data_dict['labels'][idx][1]
        else:
            label = option[0]
        new_dropdown['label'] = label
        if 'default' in data_dict:
            new_dropdown["defaults"] = [data_dict['default'][idx][1]]
        new_dropdown['parents'] = [option[0]
                                   for option in data_dict['options'][:idx]]
        new_dropdown['children'] = [option[0]
                                    for option in data_dict['options'][idx + 1:]]
        dropdown_dicts.append(new_dropdown)
    return dropdown_dicts


def get_non_dropdown_dict(data_dict):
    control_dict = {}
    for key, value in data_dict.items():
        if type(value) == list:
            for key, value in value:
                if key == 'default':
                    control_dict['defaults'] = get_default_list(value)
                elif key == 'required' and value:
                    control_dict[key] = True
                else:
                    control_dict[key] = value
        else:
            control_dict[key] = value
    return control_dict


def create_controls(widget_type, data_dict):
    control_objs = []
    print(data_dict)
    if widget_type == 'multi_tier_dropdown_widget':
        # If multi tier, multiple dropdown dicts will be created
        dropdowns_dicts = get_dropdown_dicts(data_dict)
        dropdown_objs = list(
            map(lambda x: Dropdown_Control(**x), dropdowns_dicts))
        for dropdown in dropdown_objs:
            print(dropdown)
        return dropdown_objs
    elif widget_type == 'single_multiselection_tier_dropdown_widget':
        control_dict = get_non_dropdown_dict(data_dict)
        control_obj = Dropdown_Control(**control_dict)
    elif widget_type == 'input_widget':
        input_control_dict = get_non_dropdown_dict(data_dict)
        control_obj = Input_Control(**input_control_dict)
    elif widget_type == 'textarea_widget':
        data_dict["options"].append(
            ("type", "textarea"))
        input_control_dict = get_non_dropdown_dict(data_dict)
        control_obj = Input_Control(**input_control_dict)
    elif widget_type == 'email':
        data_dict["options"].append(("type", "email"))
        input_control_dict = get_non_dropdown_dict(data_dict)
        control_obj = Input_Control(**input_control_dict)
    else:
        raise Exception(f'Unknown widget type "{widget_type}"')
    control_objs.append(control_obj)
    print(control_obj)
    return control_objs


with open("tests/sampler.tpl") as tpl_obj:
    contents = tpl_obj.read().strip()
    include_pattern = re.compile(
        r'^\s*\{include\s*file=[\'"]global/widgets/dynamic_mapping/(.*?)\}', re.DOTALL | re.MULTILINE)
    include_sections = re.findall(include_pattern, contents)
    data_sections = re.split(include_pattern, contents)
    data_sections = [x.strip() for x in data_sections[::2] if x]
    master_controls = []

    for idx, match in enumerate(include_sections):
        match = match.strip()
        widget_type = get_widget_type(match)
        print(widget_type)
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

        # Pass each widget type and corresponding data to create control instances
        master_controls.extend(create_controls(widget_type, var_data_dict))
        print(master_controls)
        # print(assigns)
        # print(assign_arrays)
        # for key, value in var_data_dict:

        # Get all includes
        # Get all arg vars
        # Inject arg vars into include dict
