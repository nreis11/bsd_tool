import { JobData } from "equest";
import { getValue } from "./helpers";

import {
  CONTROL_TYPE_DROPDOWN,
  CONTROL_TYPE_STRING,
  CONTROL_TYPE_DECIMAL,
  CONTROL_TYPE_NUMBER,
} from "./ControlMap";

export default [
  {
    name: "Function",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Function",
    filename: "Functions",
    children: ["SubFunction"],
  },
  {
    name: "SubFunction",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Sub Function",
    filename: "Functions",
    parents: ["Function"],
    requirementsMet: (controls) => getValue("Function", controls),
  },
  {
    name: "VacancyOccupations",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Occupation Type",
    filename: "Occupations",
  },
  {
    name: "VacancyLevel",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Education Level",
    filename: "Levels",
    required: true,
  },
  {
    name: "VacancySalary",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Salary Description",
    filename: "Salaries",
    required: true,
  },
  {
    name: "SalaryMin",
    type: CONTROL_TYPE_DECIMAL,
    label: "Salary Min",
    value: JobData.compensationAmount || JobData.compensationMin,
  },
  {
    name: "SalaryMax",
    type: CONTROL_TYPE_DECIMAL,
    label: "Salary Max",
    value: JobData.compensationAmount || JobData.compensationMax,
  },
  {
    name: "Region",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Region",
    filename: "Regions",
    children: ["Area"],
  },
  {
    name: "Area",
    type: CONTROL_TYPE_DROPDOWN,
    label: "Area",
    filename: "Regions",
    parents: ["Region"],
    requirementsMet: (controls) => getValue("Region", controls),
  },
  {
    name: "Zipcode",
    type: CONTROL_TYPE_STRING,
    label: "Zipcode",
    required: true,
    value: JobData.jobPostalCode,
  },
  {
    name: "VacancyAreaRadius",
    type: CONTROL_TYPE_NUMBER,
    label: "Zipcode Radius (meters)",
    required: true,
  },
];
