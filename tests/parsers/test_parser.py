import logging

from nomad.datamodel import EntryArchive
from nomad_tadf_molecules.parsers.tadf_molecules import TADFMoleculesParser


def test_parse_file():
    parser = TADFMoleculesParser()
    archive = EntryArchive()
    parser.parse('tests/data/molecule30.json', archive, logging.getLogger())
