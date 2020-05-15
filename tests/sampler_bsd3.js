import { JobData } from "equest";

import { getValue } from "./helpers";

import { CONTROL_TYPE_DROPDOWN, CONTROL_TYPE_NUMBER, CONTROL_TYPE_STRING, CONTROL_TYPE_TEXT, CONTROL_TYPE_EMAIL, CONTROL_TYPE_DATE, CONTROL_TYPE_LOCATION_LOOKUP } from "./ControlMap";

const config = [
  {
    name: "Function",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Function",
    filename: "Functions",
    required: true,
    children: ['SubFunction'],
    value: JobData.func,
  },
  {
    name: "SubFunction",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Sub Function",
    filename: "Functions",
    parents: ['Function'],
    requirementsMet: (controls) => getValue("Function", controls),
    value: "111",
  },
  {
    name: "Industry",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Industry",
    filename: "Industries",
    multi: true,
    selections: 3,
  },
  {
    name: "SalaryMin",
    type: CONTROL_TYPE_NUMBER,
    label: "Salary Min",
    value: JobData.compensationAmount || JobData.compensationMin,
  },
  {
    name: "Zipcode",
    type: CONTROL_TYPE_STRING,
    label: "Zipcode",
    required: true,
    value: JobData.jobPostalCode,
  },
  {
    name: "JobSummary",
    type: CONTROL_TYPE_TEXT,
    label: "Job Summary",
    maxLength: 400,
  },
  {
    name: "JobEmail",
    type: CONTROL_TYPE_EMAIL,
    label: "Recruiter Email Address",
    required: true,
  },
  {
    name: "ApplicationDeadline",
    type: CONTROL_TYPE_DATE,
    label: "Søknadsfristen",
    value: JobData.endDate,
  },
  {
    name: "PostingLocation",
    type: CONTROL_TYPE_LOCATION_LOOKUP,
    label: "Advertising Location",
    value: "$default_location",
  },
  {
    name: "Warning",
    type: CONTROL_TYPE_TEXT,
    label: "Warning",
    placeholder: "* Additional charges applied by board if these fields are set to yes",
    disabled: true,
  }
];

export default config;