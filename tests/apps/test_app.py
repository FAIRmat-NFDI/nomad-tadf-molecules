def test_importing_app():
    # this will raise an exception if pydantic model validation fails for th app
    from nomad_tadf_molecules.apps import myapp

