# ruff: noqa: PLR2004
import os.path

from nomad.client import normalize_all, parse


def test_tadf_schema():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)

    assert entry_archive.data.photoluminescence_quantum_yield == 0.1
    assert entry_archive.data.peak_emission_wavelength.magnitude == 400
    assert entry_archive.data.delayed_lifetime.magnitude == 3
    assert entry_archive.data.singlet_triplet_energy_splitting.magnitude == 2
