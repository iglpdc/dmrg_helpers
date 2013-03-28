.. DMRG helpers documentation master file, created by
   sphinx-quickstart on Sun Mar 10 17:44:46 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DMRG helpers's documentation!
========================================

This is documentation for a Python module used to process, analyze, and plot
the data resulting from our DMRG code. With this module, you can read a bunch
of files with estimator data at once, even if they correspond to different
Hamiltonian parameters; extract data for a particular correlator or calculate a
structure factor, and save to a file or plot your data using matplotlib.

For example, to calculate the spin structure factor for certain model, reading
the data from a file 'estimators.dat' , and saving the spin structure factor to
another file for plotting, you have to do only this: 

.. literalinclude:: _static/spin_structure_factor_from_file.py

If you want to plot the data for a given correlator, say :math:`S_{i}^{z}
S_{i+1}^{z}`, then you only have to do this:

.. literalinclude:: _static/plot_correlator_from_file.py

The `plot` contains not only the data for the correlator, but also information
about the Hamiltonian parameters and all that.

The important thing to note is that the 'estimators.dat' file in the examples
above is the raw file as it comes out from the DMRG run, without any further
processing. Therefore, it contains all the correlators that you calculated in a
given run.

Even nicer, you can pass a directory, instead of a file, to the function that
extracts the data. In this case, the code will crawl down the directory tree,
find all the estimators files, extract the data, and organize them. For
example, if you have now a directory structure that contains data for several
system lengths, the following code will make the plot for :math:`S_{i}^{z}
S_{i+1}^{z}` and all the system lengths found, labelling each curve with the
system length:

.. literalinclude:: _static/plot_correlator_from_dir.py

Contents
--------

.. toctree::
   :maxdepth: 2

   install
   about_files
   extract
   analyze


Developer Documentation
-----------------------
.. toctree::
   :maxdepth: 1
   
   _ref/dmrg_helpers

