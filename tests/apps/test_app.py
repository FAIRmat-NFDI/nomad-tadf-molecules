def test_importing_app():
    # This will raise an exception if pydantic model validation fails for the app
    from nomad_tadf_molecules.apps import tadf_molecules  # noqa: F401
