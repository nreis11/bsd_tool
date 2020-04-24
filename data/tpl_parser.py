import re
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
    matches = widget_type.findall(include_section)
    if not matches:
        raise Exception("Widget type not found")
    return matches[0]


def get_include_variable(include_section):
    include_list = re.split(r'\s+', include_section)[1:]
    include_list = list(map(lambda x: x.replace("$", ""), include_list))

    # params = list(map(lambda x: x.split('='), include_list[2:]))
    param_dict = {}
    for param in include_list:
        param_list = param.split('=')
        param_dict[param_list[0]] = param_list[1]
    print(param_dict)
    return param_dict


with open("tests/sampler.tpl") as tpl_obj:
    contents = tpl_obj.read()
    include_pattern = re.compile(
        r'^\s*\{include(.*?)\}', re.DOTALL | re.MULTILINE)

    result = re.split(include_pattern, contents)

    for idx, section in enumerate(result):
        section = section.strip()
        if idx % 2:
            # Include file
            widget_type = get_widget_type(section)
            var_data_dict = get_include_variable(section)
        else:
            # Data
            pass
        print("*******BREAK***********")
