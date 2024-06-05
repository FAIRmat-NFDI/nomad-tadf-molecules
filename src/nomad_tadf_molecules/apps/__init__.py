from nomad.config.models.plugins import AppEntryPoint

from nomad_tadf_molecules.apps.tadf_molecules import tadf_molecules_app

tadf_molecules = AppEntryPoint(
    name='TADF Molecules',
    description="""
	Search information about thermally activated delayed fluorescent (TADF)
	molecules.
	""",
    app=tadf_molecules_app,
)
