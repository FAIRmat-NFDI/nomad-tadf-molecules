# ruff: noqa: PLR2004
import logging

from nomad.datamodel import EntryArchive

from nomad_tadf_molecules.parsers.tadf_molecules import TADFMoleculesParser


def test_parse_file():
    parser = TADFMoleculesParser()
    archive = EntryArchive()
    parser.parse('tests/data/molecule30.json', archive, logging.getLogger())

    assert archive.data.photoluminescence_quantum_yield is None
    assert archive.data.peak_emission_wavelength.magnitude == 493.0
    assert archive.data.delayed_lifetime is None
    assert archive.data.singlet_triplet_energy_splitting.magnitude == 0.17
