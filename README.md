## Socio-Economic Caste Census 2011

Python script [secc.py](secc.py) scrapes all the English language data from http://164.100.129.6/netnrega/secc_list.aspx and produces [secc.csv](secc.csv) with the following columns:

`state, district, tehsil, panchayat, language, auto_inclusion_deprivation_or_exclusion_or_other ('auto_inclusion_or_deprivation is radio button is clicked, exlusion if that button is clicked, other if that button is clicked) head_of_hh, gender, age, social_cat, fathers_and_mothers_name, deprivation_count, auto_inclusion_deprivation_code, total_members, hh_summary_auto_inclusion, hh_summary_auto_exclusion, hh_summary_auto_other, hh_summary_deprivation`

Some combinations of dropdowns have no data. We have those combinations in the CSV but put an empty string in all other fields afterstarting `head_of_hh.`

### Data

The data are posted at: https://doi.org/10.7910/DVN/LIIBNB

### English Translations

You can get English translations using [Table Translator](https://github.com/in-rolls/table_word_level_translator).
