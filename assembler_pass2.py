import re

# Op codes for SIC/XE instructions
op_codes = {
    # Format 1
    'FIX': '0xC4', 'FLOAT': '0xC0', 'HIO': '0xF4', 'NORM': '0xC8', 
    'SIO': '0xF0', 'TIO': '0xF8',
    
    # Format 2
    'ADDR': '0x90', 'CLEAR': '0xB4', 'COMPR': '0xA0', 'DIVR': '0x9C', 
    'MULR': '0x98', 'RMO': '0xAC', 'SHIFTL': '0xA4', 'SHIFTR': '0xA8', 
    'SUBR': '0x94', 'SVC': '0xB0', 'TIXR': '0xB8',
    
    # Format 3/4
    'ADD': '0x18', 'COMP': '0x28', 'JEQ': '0x30', 'JLT': '0x38', 
    'JSUB': '0x48', 'LDA': '0x00', 'LDB': '0x68', 'RSUB': '0x4C', 
    'STA': '0x0C', 'STL': '0x14', 'TIX': '0x2C'
}

# Register numbers
registers = {
    'A': 0, 'X': 1, 'L': 2, 'B': 3, 'S': 4, 'T': 5, 'F': 6
}

instruction_size = {
    # Format 1
    'FIX': 1, 'FLOAT': 1, 'HIO': 1, 'NORM': 1, 'SIO': 1, 'TIO': 1,

    # Format 2
    'ADDR': 2, 'CLEAR': 2, 'COMPR': 2, 'DIVR': 2, 'MULR': 2,
    'RMO': 2, 'SHIFTL': 2, 'SHIFTR': 2, 'SUBR': 2, 'SVC': 2, 'TIXR': 2,

    # Format 3 (default to 3 if not listed)
    'LDA': 3, 'STA': 3, 'STL': 3, 'LDB': 3, 'COMP': 3, 'JEQ': 3,
    'JSUB': 3, 'RSUB': 3, 'ADD': 3, 'JLT': 3, 'TIX': 3,

    # Directives
    'START': 0, 'BASE': 0, 'END': 0,
    'RESW': 3, 'RESB': 1, 'BYTE': 1, 'WORD': 3
}

def load_symbol_table(file_path):
    symbol_table = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        symbol_table[parts[0]] = parts[1]
    except FileNotFoundError:
        print(f"Error: Symbol table file '{file_path}' not found.")
    return symbol_table

def load_location_counter(file_path):
    location_counter = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    location_counter.append(line.strip())
    except FileNotFoundError:
        print(f"Error: Location counter file '{file_path}' not found.")
    return location_counter

def format1_object_code(op_code):
    """Generate object code for Format 1 instructions"""
    return f"{int(op_code, 0):02X}"

def format2_object_code(op_code, operand):
    """Generate object code for Format 2 instructions"""
    r1, r2 = 0, 0
    if ',' in operand:
        regs = operand.split(',')
        r1 = registers.get(regs[0].strip(), 0)
        r2 = registers.get(regs[1].strip(), 0)
    else:
        r1 = registers.get(operand.strip(), 0)
    
    return f"{int(op_code, 0):02X}{r1}{r2}"

def format3_object_code(op_code, operand, symbol_table, current_address, base_address):
    """Generate object code for Format 3 instructions"""
    # Default flags
    n, i, x, b, p, e = 1, 1, 0, 0, 0, 0
    
    # Parse operand
    indexed = False
    if operand and ',' in operand:
        parts = operand.split(',')
        operand = parts[0].strip()
        if parts[1].strip().upper() == 'X':
            indexed = True
            x = 1
    
    # Check for immediate or indirect addressing
    if operand.startswith('#'):
        n, i = 0, 1  # Immediate addressing
        operand = operand[1:]
    elif operand.startswith('@'):
        n, i = 1, 0  # Indirect addressing
        operand = operand[1:]
    
    # Calculate displacement
    disp = 0
    if operand in symbol_table:
        target_address = int(symbol_table[operand], 16)
        next_instruction = int(current_address, 16) + 3  # PC points to next instruction
        
        # Try PC-relative first
        pc_disp = target_address - next_instruction
        if -2048 <= pc_disp <= 2047:
            # PC-relative addressing works
            p = 1
            disp = pc_disp & 0xFFF  # Ensure 12-bit value
        elif base_address is not None:
            # Try base-relative addressing
            base_disp = target_address - base_address
            if 0 <= base_disp <= 4095:
                b = 1
                p = 0
                disp = base_disp
            else:
                print(f"Warning: Address displacement out of range for {operand}")
                disp = 0
        else:
            print(f"Warning: Address displacement out of range for {operand}")
            disp = 0
    elif operand == '':
        # For instructions like RSUB that don't have operands
        disp = 0
    elif operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
        # For immediate values
        disp = int(operand) & 0xFFF
    elif operand.startswith('0x') or operand.startswith('0X'):
        # For hexadecimal values
        try:
            disp = int(operand, 16) & 0xFFF
        except ValueError:
            print(f"Warning: Invalid hexadecimal value {operand}")
            disp = 0
    
    # Calculate object code
    opcode_bits = int(op_code, 0) >> 2  # Discard last 2 bits
    flags = (n << 5) | (i << 4) | (x << 3) | (b << 2) | (p << 1) | e
    
    first_byte = (opcode_bits << 2) | (flags >> 4)
    second_byte = ((flags & 0xF) << 4) | ((disp >> 8) & 0xF)
    third_byte = disp & 0xFF
    
    return f"{first_byte:02X}{second_byte:02X}{third_byte:02X}"

def format4_object_code(op_code, operand, symbol_table):
    """Generate object code for Format 4 instructions"""
    # Default flags for format 4
    n, i, x, b, p, e = 1, 1, 0, 0, 0, 1  # e=1 for format 4
    
    # Parse operand
    indexed = False
    if operand and ',' in operand:
        parts = operand.split(',')
        operand = parts[0].strip()
        if parts[1].strip().upper() == 'X':
            indexed = True
            x = 1
    
    # Check for immediate or indirect addressing
    if operand.startswith('#'):
        n, i = 0, 1  # Immediate addressing
        operand = operand[1:]
    elif operand.startswith('@'):
        n, i = 1, 0  # Indirect addressing
        operand = operand[1:]
    
    # Get address
    address = 0
    if operand in symbol_table:
        address = int(symbol_table[operand], 16)
    elif operand.isdigit() or (operand.startswith('-') and operand[1:].isdigit()):
        address = int(operand) & 0xFFFFF
    elif operand.startswith('0x') or operand.startswith('0X'):
        try:
            address = int(operand, 16) & 0xFFFFF
        except ValueError:
            print(f"Warning: Invalid hexadecimal value {operand}")
            address = 0
    
    # Calculate object code
    opcode_bits = int(op_code, 0) >> 2  # Discard last 2 bits
    flags = (n << 5) | (i << 4) | (x << 3) | (b << 2) | (p << 1) | e
    
    first_byte = (opcode_bits << 2) | (flags >> 4)
    second_byte = ((flags & 0xF) << 4) | ((address >> 16) & 0xF)
    third_byte = (address >> 8) & 0xFF
    fourth_byte = address & 0xFF
    
    return f"{first_byte:02X}{second_byte:02X}{third_byte:02X}{fourth_byte:02X}"

def process_byte_directive(operand):
    """Process BYTE directive and return the object code"""
    if operand.startswith("C'") and operand.endswith("'"):
        # Character constant
        chars = operand[2:-1]
        hex_values = [f"{ord(c):02X}" for c in chars]
        return ''.join(hex_values)
    elif operand.startswith("X'") and operand.endswith("'"):
        # Hexadecimal constant
        return operand[2:-1]
    return ""

def process_word_directive(operand):
    """Process WORD directive and return the object code"""
    try:
        value = int(operand)
        return f"{value & 0xFFFFFF:06X}"
    except ValueError:
        return "000000"

def generate_object_code(instruction, operand, symbol_table, current_address, base_address=None):
    """Generate object code for an instruction"""
    instruction = instruction.upper()
    
    # Check if it's a format 4 instruction (starts with +)
    if instruction.startswith('+'):
        base_instruction = instruction[1:]
        if base_instruction in op_codes:
            return format4_object_code(op_codes[base_instruction], operand, symbol_table)
        return "ERROR"
    
    # Directives
    if instruction == 'BYTE':
        return process_byte_directive(operand)
    elif instruction == 'WORD':
        return process_word_directive(operand)
    elif instruction in ['START', 'END', 'BASE', 'RESW', 'RESB']:
        return ""
    
    # Regular instructions
    if instruction in op_codes:
        if instruction in ['FIX', 'FLOAT', 'HIO', 'NORM', 'SIO', 'TIO']:
            # Format 1
            return format1_object_code(op_codes[instruction])
        elif instruction in ['ADDR', 'CLEAR', 'COMPR', 'DIVR', 'MULR', 'RMO', 'SHIFTL', 'SHIFTR', 'SUBR', 'SVC', 'TIXR']:
            # Format 2
            return format2_object_code(op_codes[instruction], operand)
        else:
            # Format 3
            return format3_object_code(op_codes[instruction], operand, symbol_table, current_address, base_address)
    
    return ""

def pass2(intermediate_file, location_counter_file, symbol_table_file):
    """Perform pass 2 of the SIC/XE assembler"""
    # Load symbol table and location counter
    symbol_table = load_symbol_table(symbol_table_file)
    location_counter = load_location_counter(location_counter_file)
    
    # Read intermediate file
    try:
        with open(intermediate_file, 'r') as f:
            intermediate_lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Intermediate file '{intermediate_file}' not found.")
        return
    
    # Prepare output
    object_codes = []
    
    # Track BASE register value
    base_address = None
    
    # Process each line
    for i, line in enumerate(intermediate_lines):
        tokens = line.split()
        
        # Parse line
        if len(tokens) == 3:
            label, instruction, operand = tokens
        elif len(tokens) == 2:
            if tokens[0].upper() in instruction_size or tokens[0].startswith('+'):
                label = ""
                instruction, operand = tokens
            else:
                label, instruction = tokens
                operand = ""
        elif len(tokens) == 1:
            label = ""
            instruction = tokens[0]
            operand = ""
        else:
            continue  # Skip invalid lines
        
        instruction = instruction.upper()
        
        # Update BASE register if needed
        if instruction == 'BASE' and operand in symbol_table:
            base_address = int(symbol_table[operand], 16)
        
        # Generate object code
        current_address = location_counter[i] if i < len(location_counter) else "0000"
        object_code = generate_object_code(instruction, operand, symbol_table, current_address, base_address)
        object_codes.append(object_code)
    
    # Write object codes to output file
    with open('out_pass2.txt', 'w') as f:
        for code in object_codes:
            f.write(f"{code}\n")
    
    # Now generate HTME records (we'll implement this in the next step)
    generate_htme_records(intermediate_lines, location_counter, object_codes, symbol_table)

def generate_htme_records(intermediate_lines, location_counter, object_codes, symbol_table):
    """Generate HTME records for the SIC/XE program"""
    if not intermediate_lines or not location_counter or not object_codes:
        print("Error: Missing data for HTME record generation")
        return
    
    # Initialize variables
    program_name = ""
    starting_address = ""
    ending_address = ""
    text_records = []
    current_text_record = {"address": "", "length": 0, "codes": []}
    
    # Find program name and starting address
    first_line = intermediate_lines[0].split()
    if len(first_line) >= 3 and first_line[1].upper() == 'START':
        program_name = first_line[0]
        starting_address = location_counter[0]
    
    # Process each line to generate text records
    for i, (line, lc, obj_code) in enumerate(zip(intermediate_lines, location_counter, object_codes)):
        tokens = line.split()
        instruction = tokens[1] if len(tokens) > 1 else ""
        
        # Skip directives that don't generate code
        if instruction.upper() in ['START', 'END', 'BASE']:
            if instruction.upper() == 'END':
                ending_address = lc
            continue
        
        # Skip RESx directives (they create a new text record)
        if instruction.upper() in ['RESW', 'RESB'] and obj_code == "":
            if current_text_record["codes"]:
                # Save current text record
                text_records.append(current_text_record)
                # Start a new text record after this RESW/RESB
                current_text_record = {"address": "", "length": 0, "codes": []}
            continue
        
        # Skip empty object codes
        if not obj_code:
            continue
        
        # If this is the first code or we need to start a new record
        if not current_text_record["codes"]:
            current_text_record["address"] = lc
        
        # Check if adding this code would exceed maximum text record length (60 bytes)
        code_length = len(obj_code) // 2  # Convert hex string length to bytes
        if current_text_record["length"] + code_length > 30:
            # Save current text record and start a new one
            text_records.append(current_text_record)
            current_text_record = {"address": lc, "length": 0, "codes": []}
        
        # Add code to current text record
        current_text_record["codes"].append(obj_code)
        current_text_record["length"] += code_length
    
    # Add the last text record if not empty
    if current_text_record["codes"]:
        text_records.append(current_text_record)
    
    # Get program length
    program_length = int(ending_address or location_counter[-1], 16) - int(starting_address, 16)
    
    # Generate HTME records
    htme_records = []
    
    # Header record (H)
    program_name_padded = program_name.ljust(6)[:6]
    htme_records.append(f"H{program_name_padded}{starting_address}{program_length:06X}")
    
    # Text records (T)
    for record in text_records:
        if record["codes"]:
            address = record["address"]
            length = record["length"]
            object_code = ''.join(record["codes"])
            htme_records.append(f"T{address}{length:02X}{object_code}")
    
    # End record (E)
    first_executable = starting_address
    for i, line in enumerate(intermediate_lines):
        tokens = line.split()
        if len(tokens) > 1 and tokens[1].upper() not in ['START', 'BASE', 'RESW', 'RESB', 'BYTE', 'WORD']:
            first_executable = location_counter[i]
            break
    
    # Convert to integer and format as 6 hex digits
    first_exec_addr = int(first_executable, 16)
    htme_records.append(f"E{first_exec_addr:06X}")
    
    # Write HTME records to output file
    with open('HTME.txt', 'w') as f:
        for record in htme_records:
            f.write(f"{record}\n")

if __name__ == "__main__":
    # Run pass 2
    pass2('intermediate.txt', 'out_pass1.txt', 'symbTable.txt')