# Advanced Debug Console Features

The Debug Console in VS Code is an interactive REPL that runs while your program is paused at a breakpoint. It lets you execute any Python code in the context of your running program.

## Opening Debug Console

- Press `Ctrl+Shift+Y`
- Or click "Debug Console" tab in the bottom panel

## 1. Explore Objects

```python
cart                    # shows repr
cart.items              # list of dicts
cart.items[0]           # first item
cart.items[0]["name"]   # nested access
cart._discount          # access private attributes
```

## 2. Call Methods

```python
cart.get_total()                    # call method
cart.add_item("Monitor", 299.99)    # modify the cart
cart.get_total()                    # see new total
```

## 3. Use Python Built-ins

```python
dir(cart)                           # list all attributes/methods
type(cart)                          # object type
vars(cart)                          # dict of attributes
len(cart.items)                     # length
hasattr(cart, 'items')              # check attribute exists
isinstance(cart, ShoppingCart)      # type checking
```

## 4. Import Modules On-The-Fly

```python
import json
print(json.dumps(cart.items, indent=2))

import datetime
datetime.datetime.now()

import os
os.getcwd()
```

## 5. List Comprehensions & Data Processing

```python
[item["name"] for item in cart.items]
sum(item["price"] for item in cart.items)
max(cart.items, key=lambda x: x["price"])
{item["name"]: item["price"] for item in cart.items}
```

## 6. Modify State

```python
cart._discount = 0.5                # 50% off
cart.get_total()                    # see reduced total
customer_name = "Bob"               # change variable
cart.items.append({"name": "Gift", "price": 0, "qty": 1})
```

## 7. Create New Objects

```python
new_cart = ShoppingCart()
new_cart.add_item("Test", 10)
new_cart.get_total()
```

## 8. Test Exception Handling

```python
try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"Caught: {e}")
```

## 9. Inspect the Call Stack

```python
import traceback
traceback.print_stack()
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Up` / `Down` | Previous/next command history |
| `Tab` | Autocomplete variables and methods |
| `Ctrl+L` | Clear console |
| `F10` | Step Over (next line) |
| `F11` | Step Into (enter function) |
| `Shift+F11` | Step Out (exit function) |
| `F5` | Continue to next breakpoint |
| `Shift+F5` | Stop debugging |

## Debug Console vs Sidebar

| Sidebar | Debug Console |
|---------|---------------|
| View existing variables | Execute any Python code |
| Watch predefined expressions | Run ad-hoc expressions |
| Point-and-click interface | Type commands |
| Read-only view | Can modify variables |

**Rule of thumb:**
- Sidebar = passive observation (look at what exists)
- Debug Console = active interaction (run new code, change things)

## Tips

1. Use `dir(obj)` to discover available methods
2. Use `type(obj)` when unsure what something is
3. Use `vars(obj)` to see all instance attributes
4. Modify variables to test "what if" scenarios without changing code
5. Import modules to use additional tools for inspection
