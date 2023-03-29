import os

from dataclasses import dataclass
from math import ceil
from typing import List, Dict

from docxcompose.composer import Composer
from docx import Document as DocxDoc
from docxtpl import DocxTemplate
from tqdm import tqdm
from util.group import group_by_n
from src.mapping.csv_2_template_map import AttributeMap, DataEntry


@dataclass
class DocumentPopulator:
    tmp_dir: str
    output_path: str
    template_path: str
    templates_per_page: int

    def _render_template(self, data: List[DataEntry], mappings: List[AttributeMap], output_path: str):
        doc = DocxTemplate(self.template_path)
        variables = dict()

        # populate variables
        for i, data_entry in enumerate(data):
            variables.update({
                attr.template_key.format(i + 1): getattr(data_entry, attr.table_key)
                for attr in mappings
            })

        # render to document
        doc.render(variables)
        doc.save(output_path)

    def _render_tmp_documents(self, data: List[DataEntry], mappings: List[AttributeMap]) -> List[str]:
        grouped_data = list(group_by_n(data, n=self.templates_per_page))
        tmp_docs_count = ceil(len(data) / self.templates_per_page)
        tmp_docs_paths = [f"{self.tmp_dir}/{doc_index}.docx" for doc_index in range(tmp_docs_count)]

        for tmp_path, data_group in tqdm(zip(tmp_docs_paths, grouped_data)):
            self._render_template(
                data=data_group,
                mappings=mappings,
                output_path=tmp_path
            )

        return tmp_docs_paths

    def _merge_tmp_documents(self, tmp_docs_paths: List[str]):
        tmp_doc = DocxDoc(tmp_docs_paths[0])
        tmp_doc.add_page_break()
        composer = Composer(tmp_doc)

        for i, tmp_path in enumerate(tmp_docs_paths[1::]):  # Skip first because it has been already added.
            tmp_doc = DocxDoc(tmp_path)
            if i < len(tmp_docs_paths) - 2:  # no need to add page break on the last page
                tmp_doc.add_page_break()
            composer.append(tmp_doc)

        composer.save(self.output_path)

    @staticmethod
    def _remove_tmp_documents(tmp_docs_paths: List[str]):
        for tmp_path in tmp_docs_paths:  # Skip first because it has been already added.
            os.remove(tmp_path)

    def generate(self, data, mappings: List[AttributeMap]):
        tmp_docs_paths = self._render_tmp_documents(data=data, mappings=mappings)

        # merge all documents and remove temps
        self._merge_tmp_documents(tmp_docs_paths)
        DocumentPopulator._remove_tmp_documents(tmp_docs_paths)