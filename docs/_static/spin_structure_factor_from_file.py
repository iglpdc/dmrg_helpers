>>> from dmrg_helpers.extract.extract import create_db_from_file
>>> from dmrg_helpers.analyze.structure_factors import calculate_spin_struct_factor
>>> 
>>> db = create_db_from_file('estimators.dat')
>>> spin_struct_factor = calculate_spin_struct_factor(db)
>>> spin_struct_factor.save('spin_struct_factor.dat')
