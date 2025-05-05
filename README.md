# SIC/XE Assembler and Emulator

This project implements a SIC/XE assembler and emulator, which processes assembly language programs for the SIC/XE architecture. The assembler consists of two passes that generate an intermediate representation, object code, and HTME records. The emulator executes the object code, simulating the behavior of the SIC/XE machine.

## Project Structure

``` 
sicxe_assembler_corrected1/
│
├── data/
│   ├── in.txt              # Input source code
from Pass 1              
│   ├── intermediate.txt    # Output from Pass 1
│   ├── out_pass1.txt       # Location counters 
│   ├── symbTable.txt       # Symbol table from from Pass 2
│   └── out_pass2.obj          # Final object code
│   └── HTME.obj          # HTME records
│
├── src/
│   ├── instruction_set.py  # All opcodes registers, sizes
│   ├── assembler_pass1.py
│   ├── assembler_pass2.py
│
└── sicxe.py                # The main emulator file
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd sicxe_assembler
   ```

2. **Run the assembler**:
   Execute the assembler by running the `emulator.py` file:
   ```
   python src/emulator.py
   ```

## Usage Guidelines

- Place your SICXE code source file in the `src/data/in.txt`.
- The assembler will generate the intermediate file, location counter, symbol table, object code, and HTME records automatically.
- Output files will be saved in the `src/data` directory.

## Overview of SIC/XE Architecture

The Simplified Instructional Computer/Extended (SIC/XE) architecture is designed for educational purposes, providing a simplified model of a computer system. The assembler translates assembly language programs into machine code, which can be executed by the SIC/XE emulator.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
