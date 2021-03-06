import sys
import re
from data.dropdown_control import Dropdown_Control
from data.input_control import Input_Control
from data.control import Control


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
        r'\{assign var=[\'"](.*)[\'"] value=[\'"]*(.*?)[\'"]*\}')
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
    value = value.strip('\'" ')
    if '$' in value and not "$job" in value:
        print(
            f'Warning: Replace {value} with appropriate value for prop {key}')
    return (key, value)


def get_default_list(default_values):
    defaults = default_values.split('|default:')
    cleaned_defaults = []
    for default in defaults:
        parsed = default.split('|')
        value = parsed[0]
        if len(parsed) > 1:
            functions = ', '.join(parsed[1:])
            print(f'Apply {functions} to {value}')
        cleaned_defaults.append(value)
    return cleaned_defaults


def get_dropdown_dicts(data_dict):
    dropdown_dicts = []

    for idx, option in enumerate(data_dict['options']):
        new_dropdown = {'name': option[0], 'filename': data_dict['filename']}
        label = option[0]
        required = option[1]
        if required:
            new_dropdown['required'] = True
        if 'labels' in data_dict:
            for name, c_label in data_dict['labels']:
                if name == option[0]:
                    label = c_label
        new_dropdown['label'] = label
        if 'default' in data_dict:
            for name, value in data_dict["default"]:
                if name == option[0]:
                    new_dropdown["defaults"] = [value]
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


def create_controls(widget_type, data_dict, copies=1):
    control_objs = []

    # Remove unused var
    for pair in data_dict["options"]:
        if pair[0] == "nesting_level" or pair[0] == "selected":
            data_dict["options"].remove(pair)

    if widget_type == 'multi_tier_dropdown_widget':
        # If multi tier, multiple dropdown dicts will be created
        dropdowns_dicts = get_dropdown_dicts(data_dict)
        for _ in range(copies):
            control_objs.extend(list(
                map(lambda x: Dropdown_Control(**x), dropdowns_dicts)))
        return control_objs
    elif widget_type == 'single_multiselection_tier_dropdown_widget':
        control_dict = get_non_dropdown_dict(data_dict)
        control_objs.extend(get_control_copies(
            Dropdown_Control, control_dict, copies))
        return control_objs
    elif widget_type == 'input_widget':
        pass
    elif widget_type == 'textarea_widget':
        data_dict["options"].append(
            ("type", "textarea"))
    elif widget_type == 'warning_widget':
        placeholder = list(
            filter(lambda pair: pair[0] == "value", data_dict["options"]))[0][1]
        data_dict["options"] = [('name', "Warning"), ("type", "textarea"), (
            'label', "Warning"), ('placeholder', placeholder), ('disabled', True)]
    elif widget_type == 'email':
        data_dict["options"].append(("type", "email"))
    elif widget_type == 'input_date_calendar_widget':
        data_dict["options"].append(("type", "calendar"))
    elif widget_type == 'lookup_widget':
        data_dict["options"].append(("type", "lookup"))
    else:
        print(f'Unsupported widget type "{widget_type}". Skipping.')
        return []

    input_control_dict = get_non_dropdown_dict(data_dict)
    control_objs.extend(get_control_copies(
        Input_Control, input_control_dict, copies))

    return control_objs


def get_control_copies(control_class, control_dict, copies):
    control_objs = []
    for _ in range(copies):
        control_obj = control_class(**control_dict)
        control_objs.append(control_obj)
    return control_objs


def main(test=False):
    filename = get_filename(test)
    with open(filename) as tpl_obj:
        contents = tpl_obj.read().strip()
        comment_pattern = re.compile(r'\{\*.*?\*\}', re.DOTALL)
        contents = re.sub(comment_pattern, '', contents)
        include_pattern = re.compile(
            r'^\s*\{include\s*file=[\'"]global/widgets/dynamic_mapping/(.*?)\}', re.DOTALL | re.MULTILINE)
        include_sections = re.findall(include_pattern, contents)
        data_sections = re.split(include_pattern, contents)
        data_sections = [x.strip() for x in data_sections[::2] if x]
        master_controls = []

        for idx, match in enumerate(include_sections):
            match = match.strip()
            widget_type = get_widget_type(match)
            var_data_dict = get_include_variable(match)
            var_assigns = get_assign_vars(data_sections[idx])
            assign_arrays = get_assign_array_vars(data_sections[idx])
            assign_arrays.extend(var_assigns)
            copies = 1
            name_value_dict = {}

            # Check if multiple controls needed
            for pair in assign_arrays:
                if pair[0] == 'select':
                    copies = int(pair[1])
                name_value_dict[pair[0]] = pair[1]

            for key, value in var_data_dict.items():
                try:
                    var_data_dict[key] = name_value_dict[var_data_dict[key]]
                except KeyError:
                    print(
                        f'Warning: Missing {key} value for match: {match}')

            # Map lists of strings intu tuples (key, value)
            for key, value in var_data_dict.items():
                if type(value) == list:
                    var_data_dict[key] = list(map(get_tuple, value))

            # Pass each widget type and corresponding data to create control instances
            master_controls.extend(create_controls(
                widget_type, var_data_dict, copies))
        write_to_file(master_controls, test)
        return master_controls


def write_to_file(master_controls, test=False):
    if test:
        filename = "tests/sampler_result.js"
    else:
        filename = "output.js"

    with open(filename, "w") as output_file:
        output = []

        for options in Control.import_options.values():
            if options["is_required"]:
                output.append(options["text"])
        output.append(Control.get_control_types())
        master_controls_str = ",\n".join(
            list(map(lambda control: str(control), master_controls)))
        output.append(
            f'const config = [\n{master_controls_str}\n];\n\nexport default config;')

        output_file.write("\n\n".join(output))
        print(f'Successfully translated in "{filename}".')


def get_filename(test=False):
    if test:
        filename = 'tests/sampler_bsd2.tpl'
    elif len(sys.argv) < 2:
        print("Please supply a filename as argv")
        sys.exit(0)
    else:
        filename = sys.argv[1]
    print("Opening", filename)
    return filename


if __name__ == "__main__":
    main()
