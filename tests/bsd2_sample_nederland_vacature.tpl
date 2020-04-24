{include file="global/dynamic_mapping/validation.tpl"}

{assign var='filename' value="Functions"}
{assign_array var_name="dropdown_options"
    Function=""
    SubFunction=""
}
{assign_array var_name="dropdown_labels"
    Function="Function"
    SubFunction="Sub Function"
}
{include file="global/widgets/dynamic_mapping/multi_tier_dropdown_widget.tpl" filename=$filename options=$dropdown_options labels=$dropdown_labels}

{assign var='filename' value="Occupations"}
{assign_array var_name="dropdown_options"
    VacancyOccupations=""
}
{assign_array var_name="dropdown_labels"
    VacancyOccupations="Occupation Type"
}
{include file="global/widgets/dynamic_mapping/multi_tier_dropdown_widget.tpl" filename=$filename options=$dropdown_options labels=$dropdown_labels}

{assign var='filename' value="Levels"}
{assign_array var_name="dropdown_options"
    VacancyLevel="required"
}
{assign_array var_name="dropdown_labels"
    VacancyLevel="Education Level"
}
{include file="global/widgets/dynamic_mapping/multi_tier_dropdown_widget.tpl" filename=$filename options=$dropdown_options labels=$dropdown_labels}

{assign var='filename' value="Salaries"}
{assign_array var_name="dropdown_options"
    VacancySalary="required"
}
{assign_array var_name="dropdown_labels"
    VacancySalary="Salary Description"
}
{include file="global/widgets/dynamic_mapping/multi_tier_dropdown_widget.tpl" filename=$filename options=$dropdown_options labels=$dropdown_labels}

{assign_array var_name="input_options"
    name="SalaryMin"
    label="Salary Min"
    default=$job.compensation_amount.value|default:$job.compensation_range_min.value
    type="number"
    required=""
}
{include file="global/widgets/dynamic_mapping/input_widget.tpl" options=$input_options}

{assign_array var_name="input_options"
    name="SalaryMax"
    label="Salary Max"
    default=$job.compensation_amount.value|default:$job.compensation_range_max.value
    type="number"
    required=""
}
{include file="global/widgets/dynamic_mapping/input_widget.tpl" options=$input_options}

{assign var='filename' value="Regions"}
{assign_array var_name="dropdown_options"
    Region=""
    Area=""
}
{assign_array var_name="dropdown_labels"
    Region="Region"
    Area="Area"
}
{include file="global/widgets/dynamic_mapping/multi_tier_dropdown_widget.tpl" filename=$filename options=$dropdown_options labels=$dropdown_labels}

{assign_array var_name="input_options"
    name="Zipcode"
    label="Zipcode"
    default=$job.location_postalcode.value
    required="required"
}
{include file="global/widgets/dynamic_mapping/input_widget.tpl" options=$input_options}

{assign_array var_name="input_options"
    name="VacancyAreaRadius"
    label="Zipcode Radius (meters)"
    type="number"
    required="required"
}
{include file="global/widgets/dynamic_mapping/input_widget.tpl" options=$input_options}
