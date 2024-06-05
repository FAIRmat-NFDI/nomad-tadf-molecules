import json

from nomad.datamodel.datamodel import EntryArchive
from nomad.parsing.parser import MatchingParser
from nomad.units import ureg
from structlog.stdlib import BoundLogger

from nomad_tadf_molecules.schema_packages.tadf_molecules import TADFMolecule


class TADFMoleculesParser(MatchingParser):
    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger: BoundLogger,
    ) -> None:
        # Extract file contents
        with open(mainfile) as file:
            raw = json.load(file)

        # Fill information about the chemical composition
        schema_instance = TADFMolecule()
        schema_instance.DOI_number = raw['doi']
        schema_instance.name = raw['abbreviated_name']
        schema_instance.iupac_name = raw['iupac_name']
        schema_instance.smile = raw['smiles']

        # Extract the four measured properties
        for name in [
            'photoluminescence_quantum_yield',
            'peak_emission_wavelength',
            'delayed_lifetime',
            'singlet_triplet_energy_splitting',
        ]:
            value = raw.get(f'{name}_value')
            if value is not None:
                setattr(schema_instance, name, value * ureg(raw[f'{name}_unit']))

        # Save schema instance into archive.data
        archive.data = schema_instance
