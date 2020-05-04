# Goal: Build a tool to transform BSD2 pages into BSD3 pages, at least the standard ones. There are special cases which will not be handled here.

# Fields to support
multi_tier_dropdown, input_widget, textarea_widget, single_multiselection_tier_dropdown_widget, email, input_date_calendar_widget, lookup_widget

# Steps
1. Read file
 - Determine control type
 - Pass data into class constructor
 - Append to control list
2. Parse fields
3. Output BSD3 field

# USAGE
python3 setup.py filename.tpl

# Known issues
BSD2 loops should translate correctly, but num suffixes will be absent e.g. Category1, Category2
If a value is set to a variable in the `assign_array` function, the data will not be translated correctly.