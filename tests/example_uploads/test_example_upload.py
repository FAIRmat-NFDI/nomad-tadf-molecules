import os
import tempfile

from nomad.config import config


def test_example_upload():
    """Tests that the required files are created by the example upload and that
    they are processed as expected.
    """
    # We load the example upload through the config object to get the fully
    # configured object with the package installation location.
    config.load_plugins()
    example_upload_entry_point = config.get_plugin_entry_point(
        'nomad_tadf_molecules.example_uploads:tadf_molecules'
    )

    # Create a temporary directory for storing the example upload files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Load the files in the example upload entry point into the temporary
        # upload directory
        example_upload_entry_point.load(temp_dir)

        # Test that the expected files are found
        expected_filepaths = set(
            [
                'molecule30.json',
                'molecule49.json',
                'molecule76.json',
                'molecule240.json',
                'molecule316.json',
                'molecule371.json',
                'molecule678.json',
                'molecule757.json',
                'molecule924.json',
                'molecule964.json',
                'molecule1001.json',
                'molecule1040.json',
                'molecule1087.json',
                'molecule1157.json',
                'molecule1159.json',
                'molecule1197.json',
                'molecule1357.json',
                'molecule1487.json',
                'molecule1505.json',
                'molecule1531.json',
            ]
        )
        filepaths = set()
        for root, _, files in os.walk(temp_dir):
            for file in files:
                filepaths.add(os.path.relpath(os.path.join(root, file), temp_dir))
        assert filepaths == expected_filepaths
