from nomad.config.models.plugins import ExampleUploadEntryPoint

tadf_molecules = ExampleUploadEntryPoint(
    title='TADF Molecules',
    category='Examples',
    description='Set of 20 examples files for TADF Molecules',
    resources=['example_uploads/tadf_molecules/*'],
)
