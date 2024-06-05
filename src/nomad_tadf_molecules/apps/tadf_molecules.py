from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Columns,
    Dashboard,
    FilterMenu,
    FilterMenus,
    Filters,
    Format,
    Layout,
    WidgetHistogram,
    WidgetPeriodicTable,
    WidgetScatterPlot,
    WidgetTerms,
)

schema = 'nomad_tadf_molecules.schema_packages.tadf_molecules.TADFMolecule'
tadf_molecules_app = App(
    label='TADF Molecules',
    path='tadf-molecules',
    description='Search for thermally activated delayed fluorescent molecules.',
    category='Experiment',
    filters=Filters(
        include=[f'*#{schema}'],
    ),
    filters_locked={'section_defs.definition_qualified_name': schema},
    columns=Columns(
        selected=[
            'results.material.chemical_formula_hill',
            f'data.photoluminescence_quantum_yield#{schema}',
            f'data.peak_emission_wavelength#{schema}',
            f'data.delayed_lifetime#{schema}',
            f'data.singlet_triplet_energy_splitting#{schema}',
            f'data.DOI_number#{schema}',
        ],
        options={
            'results.material.chemical_formula_hill': Column(),
            f'data.photoluminescence_quantum_yield#{schema}': Column(
                format=Format(decimals=2, mode='standard')
            ),
            f'data.peak_emission_wavelength#{schema}': Column(),
            f'data.delayed_lifetime#{schema}': Column(),
            f'data.singlet_triplet_energy_splitting#{schema}': Column(),
            f'data.DOI_number#{schema}': Column(),
        },
    ),
    filter_menus=FilterMenus(
        options={
            'material': FilterMenu(label='Material'),
            'elements': FilterMenu(label='Elements / Formula', level=1, size='xl'),
            'custom_quantities': FilterMenu(label='Custom Quantities', size='l'),
            'metadata': FilterMenu(label='Visibility / IDs / Schema'),
        }
    ),
    dashboard=Dashboard(
        widgets=[
            WidgetPeriodicTable(
                type='periodictable',
                scale='linear',
                quantity='results.material.elements',
                layout={'lg': Layout(w=11, h=7, x=0, y=0)},
            ),
            WidgetScatterPlot(
                type='scatterplot',
                layout={'lg': Layout(w=7, h=7, x=11, y=0)},
                x=Axis(quantity=f'data.peak_emission_wavelength#{schema}', unit='nm'),
                y=Axis(quantity=f'data.photoluminescence_quantum_yield#{schema}'),
            ),
            WidgetTerms(
                type='terms',
                layout={'lg': Layout(w=6, h=7, x=18, y=0)},
                quantity='results.material.chemical_formula_hill',
                scale='linear',
            ),
            WidgetHistogram(
                type='histogram',
                layout={'lg': Layout(w=12, h=4, x=12, y=7)},
                autorange=True,
                nbins=30,
                scale='linear',
                quantity=f'data.delayed_lifetime#{schema}',
            ),
            WidgetHistogram(
                type='histogram',
                layout={'lg': Layout(w=12, h=4, x=12, y=7)},
                autorange=True,
                nbins=30,
                scale='linear',
                quantity=f'data.singlet_triplet_energy_splitting#{schema}',
            ),
        ]
    ),
)
