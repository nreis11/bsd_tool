from data.control import Control


class Dropdown_Control(Control):
    """This can handle single or multi-tier dropdowns with multiple selections"""

    def __init__(self, name, label, filename, required=False, parents=[], children=[], defaults=[], size=None):
        self.type = 'CONTROL_TYPE_DROPDOWN'
        Control.__init__(self, name, label, required, defaults, self.type)
        self.filename = filename
        self.parents = parents
        self.children = children
        self.selections = size
        if self.parents:
            Control.import_options["get_value"]["is_required"] = True

    def __str__(self):
        indent = ' ' * 4
        output = (
            f'  {{\n'
            f'{indent}name: "{self.name}",\n'
            f'{indent}type: {self.type},\n'
            f'{indent}label: "{self.label}",\n'
            f'{indent}filename: "{self.filename}",\n'
        )
        if self.required:
            output += f'{indent}required: true,\n'
        if self.parents:
            output += f'{indent}parents: {self.parents},\n'
            output += f'{indent}requirementsMet: (controls) => getValue("{self.parents[-1]}", controls),\n'
        if self.children:
            output += f'{indent}children: {self.children},\n'
        if self.value:
            output += f'{indent}value: {self.value},\n'
        if self.selections:
            output += f'{indent}multi: true,\n'
            output += f'{indent}selections: {self.selections},\n'

        output += f'  }}'
        return output
