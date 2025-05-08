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
    'ADD': '0x18','ADDF': '0X58','AND': '0x40', 'COMP': '0x28','COMPF': '0x88',
    'DIV': '0x24','DIVF': '0x64', 
    'J': '0x3C','JEQ': '0x30','JGT': '0x34', 'JLT': '0x38', 'JSUB': '0x48',
    'LDA': '0x00', 'LDB': '0x68', 'LDCH': '0x50','LDF': '0x70', 'LDL': '0x08','LDS': '0x6C','LDT': '0x74', 'LDX': '0x04','LPS': '0xD0', 
    'MUL': '0x20','MULF': '0x60','OR': '0x44','RD': '0xD8', 'RSUB': '0x4C', 'SSK': '0xEC',
    'STA': '0x0C','STB': '0x78', 'STCH': '0x54','STF': '0x80','STI': '0xD4', 'STL': '0x14','STS': '0x7C','STSW': '0xE8','STT': '0x84','STX': '0x10',
    'SUB': '0x1C','SUBF': '0x5C','TD': '0xE0', 'TIX': '0x2C', 'WD': '0xDC'
}

instruction_size = {
    # Format 1
    'FIX': 1, 'FLOAT': 1, 'HIO': 1, 'NORM': 1, 'SIO': 1, 'TIO': 1,

    # Format 2
    'ADDR': 2, 'CLEAR': 2, 'COMPR': 2, 'DIVR': 2, 'MULR': 2,
    'RMO': 2, 'SHIFTL': 2, 'SHIFTR': 2, 'SUBR': 2, 'SVC': 2, 'TIXR': 2,

    # Format 3 (default to 3 if not listed)
    'ADD': 3,'ADDF': 3,'AND': 3, 'COMP': 3,'COMPF': 3,
    'DIV': 3,'DIVF':3,
    'J': 3, 'JEQ': 3, 'JGT': 3,'JLT': 3, 'JSUB': 3, 
    'LDA': 3, 'LDB': 3, 'LDCH': 3,'LDF': 3, 'LDL': 3,'LDS': 3,'LDT': 3, 'LDX': 3,'LPS': 3,
    'MUL': 3,'MULF': 3,'OR': 3,'RD': 3, 'RSUB': 3,'SSK': 3, 
    'STA': 3,'STB': 3, 'STCH': 3,'STF': 3,'STI': 3, 'STL': 3,'STS': 3,'STSW': 3,'STT': 3, 'STX': 3,
    'SUB': 3,'SUBF': 3,'TD': 3, 'TIX': 3, 'WD': 3,

    # Directives
    'START': 0, 'BASE': 0, 'END': 0,
    'RESW': 3, 'RESB': 1, 'BYTE': 1, 'WORD': 3
}

registers = {
    'A': 0, 'X': 1, 'L': 2, 'B': 3, 'S': 4, 'T': 5, 'F': 6
}