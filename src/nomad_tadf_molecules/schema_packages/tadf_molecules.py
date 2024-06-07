import time

import numpy as np
from ase import Atoms
from nomad.atomutils import Formula
from nomad.datamodel.data import Schema
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.metainfo.basesections import (
    PublicationReference,
    PureSubstanceSection,
)
from nomad.datamodel.results import Material, System
from nomad.metainfo import Quantity, SchemaPackage
from nomad.normalizing.common import nomad_atoms_from_ase_atoms
from nomad.normalizing.topology import add_system, add_system_info
from rdkit import Chem
from rdkit.Chem import AllChem

m_package = SchemaPackage()


class TADFMolecule(Schema, PureSubstanceSection, PublicationReference):
    """
    A schema describing a thermally activated delayed fluorescent molecule with
    information extracted from the literature.
    """

    photoluminescence_quantum_yield = Quantity(
        type=np.float64,
        description="""
        The photoluminescence quantum yield defined as the ratio of the number
        of photons emitted to the number of photons absorbed.
        """,
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )
    peak_emission_wavelength = Quantity(
        type=np.float64,
        unit='nanometer',
        description='The wavelength at which the emission intensity is at a maximum.',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )
    delayed_lifetime = Quantity(
        type=np.float64,
        unit='microsecond',
        description="""
        The time interval between the absorption of photons (excitation) and the
        emission of light (fluorescence).
        """,
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )
    singlet_triplet_energy_splitting = Quantity(
        type=np.float64,
        unit='electron_volt',
        description='Difference in the singlet and triplet state energy levels.',
        a_eln=ELNAnnotation(
            component='NumberEditQuantity',
        ),
    )

    def normalize(self, archive, logger: None) -> None:
        # Here you can trigger base class normalization
        super().normalize(archive, logger)
        time.sleep(3)

        # Here we can trigger our own normalization
        if self.smile:
            # Convert InChi to RDkit molecule
            rdkit_mol = Chem.MolFromSmiles(self.smile)

            # Add hydrogens, store molecule formula and mass
            rdkit_mol = Chem.AddHs(rdkit_mol)
            self.molecular_formula = Chem.rdMolDescriptors.CalcMolFormula(rdkit_mol)
            self.molecular_mass = Chem.rdMolDescriptors.CalcExactMolWt(rdkit_mol)

            # Embed the molecule in 3D space and optimize its structure. Skip
            # the rest if this fails.
            AllChem.EmbedMolecule(rdkit_mol)
            try:
                AllChem.MMFFOptimizeMolecule(rdkit_mol)
            except ValueError:
                logger.warning('could not generate representative structure')
                return

            # Let's save the composition and structure into archive.results.material
            if not archive.results.material:
                archive.results.material = Material()
            formula = Formula(self.molecular_formula)
            formula.populate(archive.results.material)

            # Convert the RDKit molecule to an ASE atoms object
            positions = rdkit_mol.GetConformer().GetPositions()
            atomic_numbers = [atom.GetAtomicNum() for atom in rdkit_mol.GetAtoms()]
            ase_atoms = Atoms(numbers=atomic_numbers, positions=positions)

            # Create a System: this is a NOMAD specific data structure for
            # storing structural and chemical information that is suitable for
            # both experiments and simulations.
            system = System(
                atoms=nomad_atoms_from_ase_atoms(ase_atoms),
                label='Molecule reconstruction',
                description='3D reconstruction of the molecule generated from SMILES.',
                structural_type='molecule',
                dimensionality='0D',
            )

            # archive.results.topology can used to represent relations between
            # systems.  E.g. "System A is part of System B". In our case there
            # is only a single system.
            topology = {}
            add_system_info(system, topology)
            add_system(system, topology)
            archive.results.material.topology = list(topology.values())


m_package.__init_metainfo__()
