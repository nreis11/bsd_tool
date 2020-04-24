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

    def __str__(self):
        output = (
            f'{{\n'
            f'  name: "{self.name}"\n'
            f'  type: {self.type}\n'
            f'  label: "{self.label}"\n'
            f'  filename: "{self.filename}"\n'
        )
        if self.required:
            output += f'  required: true\n'
        if self.parents:
            output += f'  parents: {self.parents}\n'
            output += f'  requirementsMet: (controls) => getValue("{self.parents[-1]}", controls)\n'
        if self.children:
            output += f'  children: {self.children}\n'
        if self.value:
            output += f'  value: {self.value}\n'
        if self.selections:
            output += f'  multi: true\n'
            output += f'  selections: {self.selections}\n'

        output += f'}}\n'
        return output
