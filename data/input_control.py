from data.control import Control


class Input_Control(Control):
    """This can handle string, number, text area, or email inputs."""

    input_type = {
        "number": "CONTROL_TYPE_NUMBER",
        "textarea": "CONTROL_TYPE_TEXT",
        "email": "CONTROL_TYPE_EMAIL",
        "string": "CONTROL_TYPE_STRING",
        "calendar": "CONTROL_TYPE_DATE",
        "lookup": "CONTROL_TYPE_LOCATION_LOOKUP"
    }

    def __init__(self, name, label='', required=False, defaults=[], maxlength='', type="string", placeholder='', message='', disabled=False):
        self.type = Input_Control.input_type[type]
        Control.__init__(self, name, label, required, defaults, self.type)
        self.maxlength = maxlength
        self.placeholder = placeholder or message
        self.disabled = disabled

    def __str__(self):
        indent = ' ' * 4
        output = (
            f'  {{\n'
            f'{indent}name: "{self.name}",\n'
            f'{indent}type: {self.type},\n'
            f'{indent}label: "{self.label}",\n'
        )
        if self.required:
            output += f'{indent}required: true,\n'
        if self.maxlength:
            output += f'{indent}maxLength: {self.maxlength},\n'
        if self.value:
            output += f'{indent}value: {self.value},\n'
        if self.placeholder:
            output += f'{indent}placeholder: "{self.placeholder}",\n'
        if self.disabled:
            output += f'{indent}disabled: true,\n'

        output += f'  }}'
        return output
