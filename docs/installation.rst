Installation
======================

pySBOL3 is a pure `Python <https://www.python.org>`_ package and is
available on any platform that supports Python 3.  pySBOL3 requires
Python 3.6 or higher, and can be installed using using `pip
<https://pypi.org/project/pip/>`_

.. note:: Python 2 is not supported.


Install the current release
---------------------------

To install the latest release of pySBOL3 using `pip`, execute the
following line in a console or terminal:

.. code::

        pip install sbol3

If you encounter permission errors, you may want to install pySBOL3 to
your user site-packages directory as follows:

.. code::

        pip install --user sbol3

Or alternatively, you may install as a super-user (on Unix-like
platforms):

.. code::

        sudo pip install sbol3

To update pySBOL3 using pip, run:

.. code::

        pip install -U sbol3


Install the latest from GitHub
------------------------------

You can also install the latest version from GitHub. This might be
appropriate for you if you need a specific feature or bug fix that has
been fixed in git and not yet been incorporated into a release. Please
exercise caution though, the latest version might also contain new
bugs.

.. code::

        python3 -m pip install git+https://github.com/synbiodex/pysbol3


For developers
----------------------

1. Clone the repository using `git <https://git-scm.com/>`_:

.. code::

        $ git clone --recurse-submodules https://github.com/SynBioDex/sbol3.git

2. Install pySBOL3 using the ``setup.py`` file:

.. code::

        $ cd sbol3
        $ python setup.py install

3. Test the installation by importing it in a Python interpreter:

.. code::

        $ python3
	Python 3.8.5 (v3.8.5:580fbb018f, Jul 20 2020, 12:11:27)
	[Clang 6.0 (clang-600.0.57)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import sbol3
	RDFLib Version: 5.0.0


4. Optionally run the unit test suite:

.. code::

        $ python3 -m unittest discover -s test


Installing on macOS
----------------------

Macs do not ship with Python 3 so it is necessary to download and
install Python 3 before installing pySBOL3. You can download the
latest Python 3 release from `python.org
<https://www.python.org>`_. After Python 3 is installed please follow
the instructions above to install pySBOL3.

Using PyPy
----------------------

`PyPy <https://www.pypy.org>`_ is "a fast, compliant alternative
implementation of Python." PyPy uses a
`just-in-time compiler <https://en.wikipedia.org/wiki/Just-in-time_compilation>`_
(JIT), which can make certain programs faster.

pySBOL3 uses `RDFlib <https://github.com/RDFLib/rdflib>`_ which can be
slow for reading and writing SBOL files when compared to a C
implementation like `Raptor <http://librdf.org/raptor/>`_ .

Programs that might benefit from PyPy's JIT are programs that have
longer runtimes and repeat tasks. A program that iterates over a
directory reading each SBOL file, modifying the contents, and then
writing the file is a good example of a program that might benefit
from PyPy's JIT. On the other hand a program that reads or writes a
single file is an example of a program that would probably *not*
benefit from PyPy because the JIT complier doesn't have a chance to
optimize the code.

pySBOL3 is compatible with PyPy. The installation and use of PyPy is
out of scope for this document. Please see the PyPy documentation if
you want to try using PyPy with pySBOL3.
