from nomad.config.models.plugins import ParserEntryPoint


class TADFMoleculesParserEntryPoint(ParserEntryPoint):
    def load(self):
        from nomad_tadf_molecules.parsers.tadf_molecules import TADFMoleculesParser

        return TADFMoleculesParser(**self.model_dump())


tadf_molecules = TADFMoleculesParserEntryPoint(
    name='TADFMoleculesParser',
    description="""
    Used to parse information about thermally activated delayed fluorescent
    (TADF) molecules from JSON files.
    """,
    mainfile_name_re='.*molecule\d+.json',
)
