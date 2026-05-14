Usage Guide
===========

The Calculator package can be used in two ways: through the interactive
command-line interface (CLI) or programmatically via the Python API.

Command-Line Interface
----------------------

Start the interactive calculator by running:

.. code-block:: bash

   calc

You'll see the calculator prompt where you can enter expressions:

.. code-block:: text

   Calculator - Type 'help' for commands, 'quit' to exit

   calc> 5 + 3
     = 8
   calc> 10 / 4
     = 2.5
   calc> sqrt(16)
     = 4.0

Available Commands
^^^^^^^^^^^^^^^^^^

* ``help`` - Display help information
* ``history`` - Show calculation history
* ``clear`` - Clear the calculation history
* ``quit`` - Exit the calculator

Supported Operations
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Operation
     - Syntax
     - Example
   * - Addition
     - ``a + b``
     - ``5 + 3`` = 8
   * - Subtraction
     - ``a - b``
     - ``10 - 4`` = 6
   * - Multiplication
     - ``a * b``
     - ``6 * 7`` = 42
   * - Division
     - ``a / b``
     - ``15 / 3`` = 5.0
   * - Power
     - ``a ^ b``
     - ``2 ^ 8`` = 256
   * - Modulo
     - ``a % b``
     - ``17 % 5`` = 2
   * - Square Root
     - ``sqrt(n)``
     - ``sqrt(16)`` = 4.0

Python API
----------

You can also use the calculator functions directly in your Python code.

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from calculator import add, subtract, multiply, divide, power, square_root, modulo

   # Basic arithmetic
   result = add(5, 3)          # 8
   result = subtract(10, 4)    # 6
   result = multiply(6, 7)     # 42
   result = divide(15, 3)      # 5.0

   # Advanced operations
   result = power(2, 8)        # 256
   result = square_root(16)    # 4.0
   result = modulo(17, 5)      # 2

Error Handling
^^^^^^^^^^^^^^

The calculator raises ``ValueError`` for invalid operations:

.. code-block:: python

   from calculator import divide, square_root, modulo

   try:
       result = divide(10, 0)
   except ValueError as e:
       print(f"Error: {e}")  # "Cannot divide by zero"

   try:
       result = square_root(-4)
   except ValueError as e:
       print(f"Error: {e}")  # "Cannot calculate square root of a negative number"

Using Calculation History
^^^^^^^^^^^^^^^^^^^^^^^^^

Track your calculations with the history manager:

.. code-block:: python

   from calculator import CalculationHistory, add, multiply

   # Create a history instance
   history = CalculationHistory()

   # Perform calculations and add to history
   result1 = add(5, 3)
   history.add("5 + 3", result1)

   result2 = multiply(4, 7)
   history.add("4 * 7", result2)

   # Retrieve history
   all_entries = history.get_all()
   for entry in all_entries:
       print(f"{entry.expression} = {entry.result}")

   # Get last 5 entries
   recent = history.get_last(5)

   # Clear history
   history.clear()

Complete Example
^^^^^^^^^^^^^^^^

Here's a complete example combining all features:

.. code-block:: python

   from calculator import (
       add, subtract, multiply, divide,
       power, square_root, modulo,
       CalculationHistory
   )

   def calculate_with_history():
       history = CalculationHistory()

       # Perform several calculations
       operations = [
           ("15 + 27", add(15, 27)),
           ("100 - 37", subtract(100, 37)),
           ("12 * 8", multiply(12, 8)),
           ("144 / 12", divide(144, 12)),
           ("2 ^ 10", power(2, 10)),
           ("sqrt(256)", square_root(256)),
           ("100 % 7", modulo(100, 7)),
       ]

       for expression, result in operations:
           history.add(expression, result)
           print(f"{expression} = {result}")

       print(f"\nTotal calculations: {len(history)}")

   if __name__ == "__main__":
       calculate_with_history()
