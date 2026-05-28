# Specification for Calculator Programmer Mode

## Context
A planned mode for software developers, embedded engineers, and anyone working with binary or hexadecimal numbers. It coexists with Standard mode via a mode-switcher UI element that feels native to the existing dark theme.

## Core Features

### Number System Support
**Supported bases:** DEC (decimal), HEX (hexadecimal), OCT (octal), BIN (binary)

**Bitwise operations:** AND, OR, XOR, NOT, NAND, NOR, left shift `<<`, right shift `>>`

**Integer size selection:** Byte (8-bit), Word (16-bit), DWord (32-bit), QWord (64-bit)

**Default state on startup:** HEX mode active

---

## UI Layout (Top to Bottom)

### 1. Integer Size Selector
**Position:** Top of the UI, above all other panels  
**Style:** Radio buttons in horizontal row  
**Options:** Byte | Word | DWord | QWord  
**Behavior:** User can select one at a time; selection applies to all operations and displays

---

### 2. Carry Flag Indicator
**Position:** Next to the bit display (integrated into the bit display area)  
**Type:** Checkbox or LED-style indicator  
**Label:** "Carry Flag" or "C"  
**Behavior:**  
- User can manually set/clear the carry flag by clicking the checkbox
- Automatically updated by operations that generate carry (e.g., addition overflow, shifts)
- Used by "Rotate through carry" shift operation

---

### 3. Bit Display Panel
**Purpose:** Visual representation of the current value in binary with individual bit boxes

**Layout for different sizes:**
- **Byte (8-bit):** Single row of 8 bit boxes
- **Word (16-bit):** Single row of 16 bit boxes
- **DWord (32-bit):** Single row of 32 bit boxes
- **QWord (64-bit):** Single row of 64 bit boxes (horizontal scroll if needed)

**Visual Style:**
- Each bit displayed as a box (LED-style display)
- Bit grouping: Every 4 bits separated by small space (nibble grouping: `1010 1111 0000 1111`)
- Boxes labeled with bit positions (Bit 0 on the right, highest bit on the left)
- Active bit (1): highlighted/filled
- Inactive bit (0): dim/outline only

**Interaction:**
- Clicking a bit toggles it (0↔1)
- All displays (BIN/OCT/DEC/HEX text fields) update instantly when bit is toggled
- Animation: Changed bits briefly flash orange to show which bits flipped

**Accessibility:**
- Full ARIA support
- Each bit box labeled for screen readers: "Bit 7: 1", "Bit 6: 0", etc.
- Keyboard navigation: Tab/Arrow keys to navigate between bits, Space/Enter to toggle

---

### 4. HEX Panel
**Layout:** Button on left labeled "HEX" | Editable text field on right

**Button behavior:**
- Clicking HEX button activates HEX mode
- When active: button highlighted with accent color (orange/red from theme)
- All keyboard panel buttons remain enabled in HEX mode

**Text field behavior:**
- Editable: user can type directly in this field
- Updates on every keystroke
- Invalid characters silently ignored (only 0-9, A-F accepted)
- Typing in this field updates all other base displays and bit display in real-time
- Displays current value with `0x` prefix (e.g., `0xFF`)

---

### 5. DEC Panel
**Layout:** Button on left labeled "DEC" | Editable text field on right

**Button behavior:**
- Clicking DEC button activates DEC mode
- When active: button highlighted with accent color
- Disables keyboard panel buttons: A, B, C, D, E, F (these turn gray and cannot be pressed)

**Text field behavior:**
- Editable: user can type directly in this field
- Invalid characters silently ignored (only 0-9 accepted)
- Updates on every keystroke
- Displays current value without prefix (e.g., `255`)

---

### 6. OCT Panel
**Layout:** Button on left labeled "OCT" | Editable text field on right

**Button behavior:**
- Clicking OCT button activates OCT mode
- When active: button highlighted with accent color
- Disables keyboard panel buttons: A, B, C, D, E, F, 8, 9 (these turn gray)

**Text field behavior:**
- Editable: user can type directly in this field
- Invalid characters silently ignored (only 0-7 accepted)
- Updates on every keystroke
- Displays current value with `0o` prefix (e.g., `0o377`)

---

### 7. BIN Panel
**Layout:** Button on left labeled "BIN" | Editable text field on right

**Button behavior:**
- Clicking BIN button activates BIN mode
- When active: button highlighted with accent color
- Disables keyboard panel buttons: A, B, C, D, E, F, 2, 3, 4, 5, 6, 7, 8, 9 (these turn gray)

**Text field behavior:**
- Editable: user can type directly in this field
- Invalid characters silently ignored (only 0-1 accepted)
- Updates on every keystroke
- Displays current value with `0b` prefix and nibble grouping (e.g., `0b1010 1111`)

---

### 8. Bit Manipulation Panel
**Layout:** Two buttons side by side: `Bitwise` | `Bitshift`

**Bitwise Button:**
- Clicking opens floating overlay panel (2 rows × 3 columns)
- Panel size: equivalent to 2×3 button grid from keyboard panel
- Panel contents:
  - Row 1: `AND` | `OR` | `NOT`
  - Row 2: `NAND` | `NOR` | `XOR`
- Panel behavior: Auto-closes after user selects an operation
- Panel appearance: Floats above keyboard, consistent with dark theme styling

**Bitshift Button:**
- Clicking opens floating overlay panel (4 options stacked vertically)
- Panel contents (top to bottom):
  1. `Arithmetic shift`
  2. `Logical shift`
  3. `Rotate circular shift`
  4. `Rotate through carry circular shift`
- Text size: 20pt font; if text exceeds width, wraps to new line
- Panel behavior: Auto-closes after user selects an operation
- Tooltips: Each option shows brief technical definition on hover (1 line)
  - Example: "Arithmetic shift: preserves sign bit"

---

### 9. Main Display Area
**Position:** Above the keyboard panel

**Display mode:** Show full expression as it builds
- Example: `0xFF AND 0x0F OR |` (with cursor)
- Allows users to see complete expression with operators and operands

**Overflow handling:** Horizontal scroll showing rightmost (most recent) content
- User always sees what they're currently typing
- Can scroll left to see earlier parts of long expressions

**Error display:**
- Division by zero shows: `Error: Div by 0`
- Display clears on next input after error

**State persistence:**
- Internal canonical value maintained at full precision
- Each base view converts from the same canonical source (no chained conversion loss)

---

### 10. Keyboard Panel
**Layout:** 6 rows × 5 columns of buttons

#### Row 1: `A` | `<<` | `>>` | `CE` | `⌫` (backspace)
- `A`: Hexadecimal digit A
- `<<`: Left shift operator
- `>>`: Right shift operator
- `CE` (Clear Entry): Clears current number only, preserves pending operation
- `⌫` (Backspace): Delete last character

#### Row 2: `B` | `(` | `)` | `%` | `/`
- `B`: Hexadecimal digit B
- `(` `)`: Parentheses for expression grouping (full recursive nesting supported)
- `%`: Arithmetic modulo (standard division remainder)
- `/`: Division operator

#### Row 3: `C` | `7` | `8` | `9` | `*`
- `C`: Hexadecimal digit C
- `7` `8` `9`: Numeric digits
- `*`: Multiplication operator

#### Row 4: `D` | `4` | `5` | `6` | `-`
- `D`: Hexadecimal digit D
- `4` `5` `6`: Numeric digits
- `-`: Subtraction operator

#### Row 5: `E` | `1` | `2` | `3` | `+`
- `E`: Hexadecimal digit E
- `1` `2` `3`: Numeric digits
- `+`: Addition operator

#### Row 6: `F` | `+/-` | `0` | `⇄` | `=`
- `F`: Hexadecimal digit F
- `+/-`: Toggle sign (positive/negative)
- `0`: Numeric digit zero
- `⇄`: Swap operands (useful for non-commutative operations)
- `=`: Equals/execute operation

**Button styling:**
- Uniform grid, no visual separation between hex digits and numbers
- Disabled buttons (based on active base mode) turn gray and cannot be clicked
- Dark theme colors (red/orange/purple/gray) consistent with Standard mode

---

## Behavioral Specifications

### Base Mode Switching
**Active base conversion:**
- When switching between bases (e.g., HEX → DEC), the current value is converted and displayed in the new base
- Internal canonical value always maintained at full precision
- No data loss when switching bases (value preserved)

**Example flow:**
1. User types `0xFF` in HEX mode
2. User clicks DEC button
3. Display shows `255` in DEC panel
4. User clicks BIN button
5. Display shows `0b1111 1111` in BIN panel
6. All panels continue to show real-time conversions

---

### Input Validation and Overflow Handling

**During typing (overflow prevention):**
- System blocks digit entry when value would exceed current integer size
- Example: In Byte mode (max 0xFF), after typing `0xFF`, no more digits can be added
- This prevents invalid states and provides immediate feedback

**When changing integer size:**
- If value exceeds new size, it is silently truncated
- Example: `0x1234` in Word mode → switch to Byte mode → becomes `0x34`
- No error shown; truncation happens immediately

**Negative number representation:**
- Two's complement notation used for negative values
- Example: `-1` in Byte mode displays as `0xFF` (binary: `1111 1111`)
- Example: `-1` in Word mode displays as `0xFFFF` (binary: `1111 1111 1111 1111`)
- The `+/-` button toggles between positive and two's complement negative

---

### Operation Precedence and Evaluation

**Evaluation order:** Left-to-right (calculator style)
- `0x0F AND 0xFF OR 0x10` evaluates as `((0x0F AND 0xFF) OR 0x10)`
- Does not follow programming language precedence (where AND might bind tighter than OR)

**Parentheses support:**
- Full recursive nesting allowed: `((0xFF AND 0x0F) OR (0x10 XOR 0x20))`
- No depth limit on nesting

---

### Bitwise Operations

**Binary operations (AND, OR, XOR, NAND, NOR):**
- Standard two-operand operations
- Format: `operand1 OPERATOR operand2 =`
- Result respects current integer size (truncated to Byte/Word/DWord/QWord)

**NOT operation (unary):**
- Operates on current display value immediately
- User enters `0x0F`, clicks NOT, display instantly shows `0xF0` (in Byte mode)
- No second operand or `=` required
- Result depends on integer size:
  - Byte: `NOT 0x0F = 0xF0`
  - Word: `NOT 0x0F = 0xFFF0`

---

### Shift Operations

**Shift amount base:**
- Shift amount respects the current base mode
- In HEX mode: `0x0F << 0x3` shifts left by 3
- In DEC mode: `15 << 3` shifts left by 3
- Be careful: in HEX mode, `0x10` = 16 decimal

**Shift overflow behavior:**
- Shift amounts exceeding integer size are wrapped (modulo bit width)
- Example: Byte mode (8-bit), shift by 10 becomes shift by 2 (10 % 8)
- Matches x86 processor behavior

**Shift types:**

1. **Arithmetic shift right:**
   - Sign-extends (fills with sign bit)
   - Preserves negative values
   - Example (Byte): `0xFF >> 1 = 0xFF` (if treated as signed -1)
   - Example (Byte): `0x7F >> 1 = 0x3F` (if treated as unsigned 127)

2. **Logical shift:**
   - Always zero-fills
   - Example: `0xFF >> 1 = 0x7F`

3. **Rotate circular shift:**
   - Bits shifted out one end appear at the other end
   - Example (Byte): `0xFF << 1 = 0xFF` (rotate left)
   - Example (Byte): `0x81 >> 1 = 0xC0` (rotate right: `1000 0001` → `1100 0000`)

4. **Rotate through carry circular shift:**
   - Like rotate, but the carry flag is inserted into the bit stream
   - Carry flag bit is shifted into the value; bit shifted out goes to carry
   - Example (Byte with carry=0): `0x81 >>RCR 1` → value becomes `0x40`, carry becomes `1`

---

### Mode Switching (Standard ↔ Programmer)

**Switching from Standard to Programmer mode:**
- Current numeric value is preserved
- Pending operation is cleared
- Example: In Standard mode showing `15 +`, switch to Programmer → displays `0x0F` (in HEX), but the `+` operation is dropped

**Switching from Programmer to Standard mode:**
- Current numeric value converted to decimal and preserved
- Operation state cleared

---

### History Panel Integration

**History in Programmer mode:**
- History entries store the original base and integer size
- Display format: `0xFF AND 0x0F = 0x0F [HEX, Byte]`
- Each entry shows:
  - Full expression
  - Result
  - Base used (HEX/DEC/OCT/BIN)
  - Integer size (Byte/Word/DWord/QWord)

**History persistence:**
- History shared between Standard and Programmer modes (single history list)
- Entries from different modes clearly distinguished by format

---

### Swap Operation

**Swap button (`⇄`) behavior:**
- Swaps the two most recent operands in a binary operation
- Useful for non-commutative operations (subtraction, division, shift)
- Example: User enters `0x10 - 0x05`, then presses `⇄` → expression becomes `0x05 - 0x10`
- Only active when a binary operation is pending

---

## Keyboard Shortcuts

**Full keyboard support for power users:**

**Numeric input:**
- `0-9`: Digit keys
- `A-F`: Hexadecimal digits (automatically input A-F)

**Operators:**
- `+` `-` `*` `/` `%`: Arithmetic operators
- `(` `)`: Parentheses
- `Enter` or `=`: Execute operation
- `Backspace`: Delete last character
- `Escape`: Clear entry (CE equivalent)

**Base mode switching:**
- `F2`: Switch to HEX mode
- `F3`: Switch to DEC mode
- `F4`: Switch to OCT mode
- `F5`: Switch to BIN mode

**Advanced:**
- `Ctrl+Shift+X`: Swap operands

---

## Visual Theme and Styling

**Color scheme:**
- Same dark theme as Standard mode (red/orange/purple/gray)
- Consistent visual identity across modes
- No color scheme change when switching between Standard and Programmer modes

**Active state indicators:**
- Active base button (HEX/DEC/OCT/BIN): highlighted with orange/red accent color
- Disabled buttons (wrong base): grayed out at 50% opacity, not clickable
- Pending operation: shown in expression display

**Panel styling:**
- Floating overlay panels (Bitwise/Bitshift) use same dark theme
- Panels have subtle shadow/border to indicate they're floating
- Button grid in panels matches keyboard panel styling

---

## Animations and Feedback

**Bit flip animation:**
- When bits change due to an operation, changed bits briefly flash orange (300ms duration)
- Helps users see which bits were affected by the operation

**Button press feedback:**
- Standard button press animation (slight scale or color change)
- Consistent with Standard mode button behavior

---

## State Persistence

**Remember between sessions:**
- Last used mode (Standard vs Programmer)
- Last used base (HEX/DEC/OCT/BIN)
- Last used integer size (Byte/Word/DWord/QWord)
- Carry flag state

**On startup:**
- Restore full state from previous session
- If no prior session, default to Programmer mode with HEX and DWord

---

## First-Use Experience

**Tutorial overlay on first switch to Programmer mode:**
- Brief overlay highlighting key features:
  - "Select your number base here" (points to HEX/DEC/OCT/BIN buttons)
  - "Visual bit representation" (points to bit display)
  - "Advanced operations" (points to Bitwise/Bitshift panel)
- Dismissible with "Got it" button or by clicking anywhere
- Only shown once (tracked in persistent settings)

---

## Accessibility

**Screen reader support:**
- All buttons have descriptive ARIA labels
- Bit display boxes announce position and state: "Bit 7, value 1"
- Mode changes announced: "Switched to Hexadecimal mode"
- Operation results announced: "Result: 0xFF"

**Keyboard navigation:**
- Full keyboard control without mouse
- Tab order: Size selector → Carry flag → Bit display → Base buttons → Display → Keyboard panel → Operation panels
- Arrow keys navigate within bit display
- Enter/Space activates buttons

**High contrast support:**
- Respect system high contrast settings
- Ensure disabled buttons have sufficient contrast difference from enabled buttons

---

## Technical Implementation Notes

**Internal representation:**
- Store value as canonical 64-bit integer internally
- Apply current integer size as a mask during operations
- Separate "display base" from "internal value"

**Real-time updates:**
- All base conversion fields update on every keystroke
- Debouncing not required (conversions are fast)
- Bit display updates synchronously with value changes

**Parentheses parsing:**
- Implement full expression parser with recursive descent or shunting-yard algorithm
- Support unlimited nesting depth (practical limit based on display width)

**Error handling:**
- Division by zero: Display error message, clear on next input
- Invalid input: Silently ignore (don't add to field)
- Overflow during typing: Block additional digit entry

---

## Future Enhancements (Post-MVP)

**Potential additions not in initial scope:**
- Memory registers (M+, M-, MR, MC)
- Bitwise operation history/undo
- Export calculation history as text
- Programmable functions or macros
- Support for floating-point (IEEE 754) operations
- Additional bases (Base64, custom bases)

---

## Summary of Key Decisions

| Aspect | Decision |
|--------|----------|
| Base switching behavior | Convert and display in new base (preserve value) |
| Operation precedence | Left-to-right evaluation (calculator style) |
| Overflow on size change | Silently truncate to new size |
| Panel auto-close | Auto-close after operation selection |
| Shift overflow | Wrap shift amount (modulo bit width) |
| Negative numbers | Two's complement representation |
| NOT operation | Immediate (operate on display value) |
| Active base indicator | Highlight with accent color |
| Panel layout | Overlay floats above keyboard |
| Shift tooltips | Brief technical definition (1 line) |
| Button grouping | Uniform grid, no visual separation |
| Multi-hop conversion | Always convert from canonical value |
| History format | Store and display with original base and size |
| Carry flag | Show as checkbox/indicator in UI (user can set) |
| Overflow timing | Prevent during typing (block digit entry) |
| Shift amount base | Respects current base mode |
| Parentheses depth | Full recursive nesting (unlimited) |
| Modulo behavior | Arithmetic modulo (standard) |
| Size selector UI | Radio buttons horizontal row |
| Mode transition | Preserve value, clear operation |
| Live conversion | Update on every keystroke |
| CE scope | Clears current number only, preserves operation |
| Binary visualization | Individual bit boxes (LED display) |
| Keyboard shortcuts | Full support (F2-F5 for bases, etc.) |
| Binary grouping | Group by 4 bits (nibbles) |
| Interactive bits | Clicking toggles bits and updates displays |
| State persistence | Restore full state on startup |
| Arithmetic shift sign | Sign-extend (fill with sign bit) |
| Operand swap | Swap button (⇄) in keyboard panel |
| Swap position | Replace empty space in row 6 |
| Division by zero | Show error in display, clear on next input |
| Carry flag position | Next to bit display |
| Accessibility | Full ARIA support with bit positions announced |
| Color scheme | Same dark theme across modes |
| Display overflow | Horizontal scroll, show rightmost |
| Base text input | Editable (can type directly in any base field) |
| Expression display | Show full expression as it builds |
| First-use help | Brief tutorial overlay on first use |
| Bit layout (64-bit) | Single row with horizontal scroll |
| Bit animation | Highlight changed bits (flash orange) |
| Tooltip detail | Brief technical definition (1 line) |
| Invalid input | Silently ignore invalid characters |

---

## End of Specification

This specification is comprehensive and ready for implementation. All major questions about behavior, UI layout, interactions, and edge cases have been addressed.
