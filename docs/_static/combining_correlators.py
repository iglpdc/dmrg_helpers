>>> from dmrg_helpers.extract.extract import create_db_from_file
>>> 
>>> db = create_db_from_file('estimators.dat')
>>> zz_component = db.get_estimator('S_z_i*S_z_i+1')
>>> pm_component = db.get_estimator('S_p_i*S_m_i+1')
>>> mp_component = db.get_estimator('S_m_i*S_p_i+1')
>>> 
>>> correlator = zz_component + 0.5 * (pm_component + mp_component)
>>> plot = correlator.plot()
