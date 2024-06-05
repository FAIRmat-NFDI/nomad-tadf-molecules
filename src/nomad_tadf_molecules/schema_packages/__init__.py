from nomad.config.models.plugins import SchemaPackageEntryPoint


class TADFMoleculesSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    def load(self):
        from nomad_tadf_molecules.schema_packages.tadf_molecules import m_package

        return m_package


tadf_molecules = TADFMoleculesSchemaPackageEntryPoint(
    name='TADF molecules',
    description='Schema package for thermally activated delayed fluorescent (TADF) molecules.',
)
