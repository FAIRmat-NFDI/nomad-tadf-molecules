from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Dashboard,
    Format,
    Layout,
    Menu,
    MenuItemHistogram,
    MenuItemPeriodicTable,
    MenuItemTerms,
    Pagination,
    SearchQuantities,
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
    search_quantities=SearchQuantities(
        include=[f'*#{schema}'],
    ),
    filters_locked={'section_defs.definition_qualified_name': schema},
    pagination=Pagination(
        order_by=f'data.photoluminescence_quantum_yield#{schema}',
        order='desc',
    ),
    columns=[
        Column(search_quantity='results.material.chemical_formula_hill', selected=True),
        Column(
            search_quantity=f'data.photoluminescence_quantum_yield#{schema}',
            format=Format(decimals=2),
            selected=True,
        ),
        Column(
            search_quantity=f'data.peak_emission_wavelength#{schema}',
            format=Format(decimals=2),
            selected=True,
        ),
        Column(
            search_quantity=f'data.delayed_lifetime#{schema}',
            format=Format(decimals=2),
            selected=True,
        ),
        Column(
            search_quantity=f'data.singlet_triplet_energy_splitting#{schema}',
            format=Format(decimals=2),
            selected=True,
        ),
        Column(search_quantity='references', selected=True),
    ],
    menu=Menu(
        items=[
            Menu(
                title='Elements / Formula',
                size='xxl',
                items=[
                    MenuItemPeriodicTable(
                        search_quantity='results.material.elements',
                    ),
                    MenuItemTerms(
                        search_quantity='results.material.chemical_formula_hill',
                        options=0,
                    ),
                    MenuItemHistogram(
                        x='results.material.n_elements',
                    ),
                ],
            ),
            Menu(
                title='TADF Properties',
                items=[
                    MenuItemHistogram(
                        x=f'data.photoluminescence_quantum_yield#{schema}',
                    ),
                    MenuItemHistogram(
                        x=f'data.peak_emission_wavelength#{schema}',
                    ),
                    MenuItemHistogram(
                        x=f'data.delayed_lifetime#{schema}',
                    ),
                    MenuItemHistogram(
                        x=f'data.singlet_triplet_energy_splitting#{schema}',
                    ),
                ],
            ),
        ]
    ),
    dashboard=Dashboard(
        widgets=[
            WidgetPeriodicTable(
                scale='linear',
                search_quantity='results.material.elements',
                layout={'lg': Layout(w=11, h=7, x=0, y=0)},
            ),
            WidgetScatterPlot(
                layout={'lg': Layout(w=7, h=7, x=11, y=0)},
                x=dict(
                    search_quantity=f'data.peak_emission_wavelength#{schema}', unit='nm'
                ),
                y=dict(search_quantity=f'data.delayed_lifetime#{schema}'),
            ),
            WidgetTerms(
                layout={'lg': Layout(w=6, h=7, x=18, y=0)},
                search_quantity='results.material.chemical_formula_hill',
                scale='linear',
            ),
            WidgetHistogram(
                layout={'lg': Layout(w=12, h=4, x=12, y=7)},
                autorange=False,
                nbins=30,
                scale='1/4',
                x=Axis(search_quantity=f'data.delayed_lifetime#{schema}'),
            ),
            WidgetHistogram(
                layout={'lg': Layout(w=12, h=4, x=12, y=7)},
                autorange=False,
                nbins=30,
                scale='linear',
                x=dict(
                    search_quantity=f'data.singlet_triplet_energy_splitting#{schema}',
                    unit='joule',
                ),
            ),
        ]
    ),
)
