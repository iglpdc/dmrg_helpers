from dmrg_helpers.extract.extract import create_db_from_dir

db = create_db_from_dir('./results')
correlator = db.get('S_z_i*S_z_i+1')
plot = correlator.plot(label = 'L')
