{include file="global/dynamic_mapping/validation.tpl"}

{* DROPDOWN - MULTI TIER *}
{assign var='filename' value="Functions"}
{assign_array var_name="dropdown_options"
    Function="required"
    SubFunction=""
}
{assign_array var_name="dropdown_labels"
    Function="Function"
    SubFunction="Sub Function"
}
{assign_array var_name="dropdown_defaults"
    Function=$job.function.value
    SubFunction="111"
}
{include file="global/widgets/dynamic_mapping/multi_tier_dropdown_widget.tpl" filename=$filename options=$dropdown_options labels=$dropdown_labels $default=$dropdown_defaults}
{* DROPDOWN - SINGLE TIER MULTI SELECTION *}
{assign var='filename' value='Industries'}
{assign_array var_name="dropdown_options"
    name="Industry"
    label="Industry"
    size="3"
}
{include file="global/widgets/dynamic_mapping/single_multiselection_tier_dropdown_widget.tpl"
    filename=$filename
    options=$dropdown_options
}
{* NUMBER *}
{assign_array var_name="input_options"
    name="SalaryMin"
    label="Salary Min"
    default=$job.compensation_amount.value|default:$job.compensation_range_min.value
    type="number"
    required=""
}
{include file="global/widgets/dynamic_mapping/input_widget.tpl" options=$input_options}
{* STRING *}
{assign_array var_name="input_options"
    name="Zipcode"
    label="Zipcode"
    default=$job.location_postalcode.value
    required="required"
}
{include file="global/widgets/dynamic_mapping/input_widget.tpl" options=$input_options}
{* TEXT *}
{assign_array var_name="manexp_options"
    name="JobSummary"
    label="Job Summary"
    maxlength="400"
}
{include file="global/widgets/dynamic_mapping/textarea_widget.tpl" options=$manexp_options}

{* EMAIL *}
{assign_array var_name="options"
    name="JobEmail"
    label="Recruiter Email Address"
    required="required"
}
{include file="global/widgets/dynamic_mapping/email.tpl" options=$options}

{* CALENDAR *}
{assign_array var_name="calendar_options"
    name="ApplicationDeadline"
    label="Søknadsfristen"
    default=$job.end_date.value
}

{include file="global/widgets/dynamic_mapping/input_date_calendar_widget.tpl" options=$calendar_options}

{* LOOKUP *}
{assign_array var_name="lookup_options"
    label="Advertising Location"
    name="PostingLocation"
    default=$default_location
}
{include file="global/widgets/dynamic_mapping/lookup_widget.tpl" options=$lookup_options}