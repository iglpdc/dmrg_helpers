Analyzing extracted data
========================

Once you have extracted the data for some correlators, you may need to perform
extra analysis before plotting or saving. There are two things that you can do
with this package: calculate structure factors, and performing arithmetic
operations among correlators.

Calculating structure factors and Fourier transforms
----------------------------------------------------

There are several functions available in the analyze module to calculate
structure factors and, in general, perform Fourier transforms of the extracted
data. These functions take care of extracting the data from the database and
performing the mathematical operations needed.

For example, to calculate the spin structure factor, you just call the right
function: 

.. literalinclude:: _static/spin_structure_factor_from_file.py

See the documentation of the analyze module to see what's available.

Combining correlators
---------------------

Sometimes the correlator cannot be measured directly in DMRG because is a
linear combination of correlators. In this case, you measure all the
correlators needed in the DMRG and then make the linear combination in the
analysis step.

For example, to calculate :math:`\vec{S}_{i}\cdot\vec{S}_{i+1}`, you measure
the three components in the DMRG and make the linear combination here:

.. literalinclude:: _static/combining_correlators.py

