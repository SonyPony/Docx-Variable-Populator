import sys

from typing import List
from loader.exception import UnsupportedFileError
from mapping.csv_2_template_map import AttributeMap, DataEntry
from document.doc_populator import DocumentPopulator
from loader import DataLoader, MappingLoader, Config, ConfigLoader
from mapping.validator import MissingMappingKeyError, UnknownMappingKeyError, InvalidRootContainerError


def main():
    try:
        config_loader = ConfigLoader(path="../config/config.yaml")
        mapping_loader = MappingLoader(path="../config/mappings.yaml")

        # Load all configs (mapping from excel columns to document template variables, input and output filepaths).
        mappings: List[AttributeMap] = mapping_loader.load()
        config: Config = config_loader.load()

        # Load data into panda frame and format it.
        data_loader = DataLoader(path=config.data_path)
        data = data_loader.load()

    except (
            MissingMappingKeyError, UnknownMappingKeyError,
            InvalidRootContainerError, UnsupportedFileError
    ) as e:
        print(e, file=sys.stderr)
        exit(1)

    # Reformat data into Person data structures
    formatted_data = [
        DataEntry(entry)
        for entry in data.to_dict(orient="records")
    ]

    # Generate the documents.
    document_populator = DocumentPopulator(
        tmp_dir=config.tmp_dir,
        output_path=config.output_path,
        template_path=config.template_path,
        templates_per_page=config.templates_per_page
    )

    document_populator.generate(data=formatted_data, mappings=mappings)


if __name__ == "__main__":
    main()