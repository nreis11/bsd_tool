class Control():

    job_data_map = {
        "$job.classification_time.value": "JobData.classificationTime",
        "$job.classification_type.value": "JobData.classificationType",
        "$job.company_city.value": "JobData.companyCity",
        "$job.company_country.value": "JobData.companyCountry",
        "$job.company_department.value": "JobData.companyDepartment",
        "$job.company_division.value": "JobData.companyDivision",
        "$job.company_fax.value": "JobData.companyFax",
        "$job.company_name.value": "JobData.companyName",
        "$job.company_phone.value": "JobData.companyPhone",
        "$job.company_postalcode.value": "JobData.companyPostalCode",
        "$job.company_stateprovince.value": "JobData.companyState",
        "$job.company_streetaddress.value": "JobData.companyStreetAddress",
        "$job.compensation_amount.value": "JobData.compensationAmount",
        "$job.compensation_currency.value": "JobData.compensationCurrency",
        "$job.compensation_range_max.value": "JobData.compensationMax",
        "$job.compensation_range_min.value": "JobData.compensationMin",
        "$job.compensation_type.value": "JobData.compensationType",
        "$job.contact_email.value": "JobData.contactEmail",
        "$job.contact_name.value": "JobData.contactName",
        "$job.customer.value": "",
        "$job.education.value": "JobData.education",
        "$job.end_date.value": "JobData.endDate",
        "$job.function.value": "JobData.func",
        "$job.industry.value": "JobData.industry",
        "$job.io_number.value": "",
        "$job.id.value": "JobData.id",
        "$job.location_city.value": "JobData.jobCity",
        "$job.location_country.value": "JobData.jobCountry",
        "$job.location_postalcode.value": "JobData.jobPostalCode",
        "$job.location_stateprovince.value": "JobData.location",
        "$job.location_us_areacode.value": "JobData.jobAreaCode",
        "$job.recruiter_email.value": "",
        "$job.recruiter_name.value": "",
        "$job.recruiter_org.value": "",
        "$job.reply_to.value": "",
        "$job.requisition_number.value": "JobData.requisition",
        "$job.start_date.value": "JobData.startDate",
        "$job.telecommute_percentage.value": "JobData.telecommutePercentage",
        "$job.timestamp.value": "",
        "$job.travel_percentage.value": "JobData.travelPercentage",
        "$job.benefits.value": "JobData.benefits",
        "$job.company_description.value": "JobData.companyDescription",
        "$job.company_description.en": "JobData.companyDescription",
        "$job.description.value": "JobData.description",
        "$job.description_en.value": "JobData.description",
        "$job.skills.value": "JobData.skills",
        "$job.skills_en.value": "JobData.skills",
        "$job.title.en": "JobData.title"
    }

    control_types = []

    import_options = {
        "job_data": {"is_required": False, "text": 'import { JobData } from "equest";'},
        "get_value": {"is_required": False, "text": 'import { getValue } from "./helpers";'}
        # "control_types": {"is_required": True, "text": f'import {get_control_types()} from "./ControlMap";'}
    }

    def __init__(self, name, label, required, defaults, control_type):
        self.name = name
        self.label = label or name
        self.required = required
        self.value = Control.get_formmatted_value(defaults)

        if control_type not in Control.control_types:
            Control.control_types.append(control_type)

    @classmethod
    def get_value(cls, default):
        """Map bsd2 job data to bsd3, otherwise return unmodified value."""
        if default in cls.job_data_map:
            cls.import_options["job_data"]["is_required"] = True
            return cls.job_data_map[default]
        return f'"{default}"'

    @classmethod
    def get_control_types(cls):
        """Format control imports as str."""
        control_types = ", ".join(cls.control_types)
        import_str = f'import {{ {control_types} }} from "./ControlMap";'
        return import_str

    @staticmethod
    def get_formmatted_value(value_list):
        """Format default list into proper mappings ($job -> JobData) or return value unchanged as str."""
        return " || ".join([Control.get_value(value) for value in value_list])
