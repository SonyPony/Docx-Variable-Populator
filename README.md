# Docx-Variable-Populator

This repository contains a script which populates data from a `.csv` file to a `.docx` document. Variables in the document has to be in following format `{{variable_name}}` (e.g. `{{test}}`, `{{name_1}}`).

## Install
Firstly, install `Python 3.9` and then run following command:
```
pip install -r requirements.txt
```

## Run
### 1. Creating a template document
Create document template in `.docx` format. You can skip this step and use `resource/templates/template.docx` as en example.

![image](https://user-images.githubusercontent.com/8584106/228632873-7894e24e-d30a-45d7-ba94-b23fd26e0934.png)

### 2. Creating a data file
Create a table containing the data which will be used to populate the template (See example `resource/data/sample_input.csv`). The data file has to be in `.csv` format woth `;` as a delimiter.

![image](https://user-images.githubusercontent.com/8584106/228633346-9afde894-712f-40b0-a1fc-5ad699c5e759.png)

### 3. Defining mappings between data table columns and template variables
Modify `config/mappings.yaml` file to define mapping from the table columns to the document template variables. **Each mapping has to be seperated by `-` symbol** (`config/mappings.yaml` file is already filled with example mappings).  `{}` will be replaced by a subindex of a template in the given document. If the document contains multiple templates (NAME_1, NAME_2, NAME_3) the subindex will range from 1 to 3. **The `templates_per_page` has to be set to 3** in this case.
Given following mappings as an example:
```
-
    table_key: FirstName
    template_key: FNAME_{}  # {} will be formatted using subindex.
-
    table_key: LastName
    template_key: LNAME_{}  # {} will be formatted using subindex.
```
and the following data:
| FirstName | LastName |
|-----------|----------|
| Adam      | Podojný  |
| Tomáš     | Hu       |

The template variables would populate as follows:

```
FNAME_1 -> Adam
LNAME_1 -> Podojný
FNAME_2 -> Tomáš
LNAME_2 -> Hu
```

### 4. Defining the config (paths)
`config/config.yaml` defines `template_path`, `data_path`, `output_path` and `templates_per_page`.

Example of a config file:

```
# All paths are relative to the project directory.

# Directory where temporally documents will be stored (they're deleted after merging).
tmp_directory: ../resource/tmp

# Path to the document template.
template_path: ../resource/templates/template.docx

# Path to the data which will be populated in the templates.
data_path: ../resource/data/sample_input.csv

# Path where the resulting document will be stored.
output_path: ../output.docx

# How many templates are on a single page? (TEAM_1) -> 1, (TEAM_1, TEAM_2) -> 2
templates_per_page: 4   # How many persons/templates per one page?
```

### 5. Running
To run the script use following command: 

```
python src/generate_id_cards.py
```
