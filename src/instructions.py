# filepath: src/instructions.py

op_codes = {
    # Format 1
    'FIX': '0xC4', 'FLOAT': '0xC0', 'HIO': '0xF4', 'NORM': '0xC8', 
    'SIO': '0xF0', 'TIO': '0xF8',
    
    # Format 2
    'ADDR': '0x90', 'CLEAR': '0xB4', 'COMPR': '0xA0', 'DIVR': '0x9C', 
    'MULR': '0x98', 'RMO': '0xAC', 'SHIFTL': '0xA4', 'SHIFTR': '0xA8', 
    'SUBR': '0x94', 'SVC': '0xB0', 'TIXR': '0xB8',
    
    # Format 3/4
    'ADD': '0x18', 'COMP': '0x28', 'J': '0x3C', 'JEQ': '0x30', 'JLT': '0x38', 
    'JSUB': '0x48', 'LDA': '0x00', 'LDB': '0x68', 'LDCH': '0x50', 'LDL': '0x08', 'LDX': '0x04', 
    'RD': '0xD8', 'RSUB': '0x4C', 'STA': '0x0C', 'STCH': '0x54', 'STL': '0x14',
    'STX': '0x10', 'TD': '0xE0', 'TIX': '0x2C', 'WD': '0xDC'
}

instruction_size = {
    # Format 1
    'FIX': 1, 'FLOAT': 1, 'HIO': 1, 'NORM': 1, 'SIO': 1, 'TIO': 1,

    # Format 2
    'ADDR': 2, 'CLEAR': 2, 'COMPR': 2, 'DIVR': 2, 'MULR': 2,
    'RMO': 2, 'SHIFTL': 2, 'SHIFTR': 2, 'SUBR': 2, 'SVC': 2, 'TIXR': 2,

    # Format 3 (default to 3 if not listed)
    'ADD': 3, 'COMP': 3, 'J': 3, 'JEQ': 3, 'JLT': 3, 'JSUB': 3, 
    'LDA': 3, 'LDB': 3, 'LDCH': 3, 'LDL': 3, 'LDX': 3, 'RD': 3, 'RSUB': 3, 
    'STA': 3, 'STCH': 3, 'STL': 3, 'STX': 3, 'TD': 3, 'TIX': 3, 'WD': 3,

    # Directives
    'START': 0, 'BASE': 0, 'END': 0,
    'RESW': 3, 'RESB': 1, 'BYTE': 1, 'WORD': 3
}

registers = {
    'A': 0, 'X': 1, 'L': 2, 'B': 3, 'S': 4, 'T': 5, 'F': 6
}