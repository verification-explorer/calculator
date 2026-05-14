Installation Guide
==================

This guide covers how to install the Calculator package for both usage and
development.

Requirements
------------

* Python 3.10 or higher
* pip (Python package installer)

Basic Installation
------------------

For regular usage, you can install the package directly:

.. code-block:: bash

   pip install calculator

Development Installation
------------------------

For development, clone the repository and install in editable mode with
development dependencies:

.. code-block:: bash

   git clone <repository-url>
   cd calculator
   pip install -e ".[dev]"

This installs the package in editable mode (changes to source code are
immediately reflected) along with development tools:

* **pytest**: Test framework
* **pytest-cov**: Test coverage plugin
* **sphinx**: Documentation generator
* **sphinx-rtd-theme**: Read the Docs theme for Sphinx

Building Documentation
----------------------

After installing with development dependencies, build the HTML documentation:

.. code-block:: bash

   cd docs
   make html

On Windows without make:

.. code-block:: bash

   cd docs
   sphinx-build -b html . _build/html

The built documentation will be available at ``docs/_build/html/index.html``.

Verifying Installation
----------------------

Verify the installation by running the test suite:

.. code-block:: bash

   pytest tests/ -v

Or by starting the calculator:

.. code-block:: bash

   calc

You should see the calculator prompt:

.. code-block:: text

   Calculator - Type 'help' for commands, 'quit' to exit

   calc>
