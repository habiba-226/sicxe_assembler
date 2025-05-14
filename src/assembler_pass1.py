from src.instructions import instruction_size, op_codes


symbol_table = {}

def get_size(instruction, operand):
    instruction = instruction.upper()

    if instruction.startswith('+'):
        base_instruction = instruction[1:].upper()
        if base_instruction in instruction_size:
            return 4
        return 3
    
    if instruction in ['LITLD', 'LITAD', 'LITSB', 'LITCMP']:
        return 4

    if instruction == 'RESW':
        try:
            return int(operand) * 3
        except:
            return 0
    elif instruction == 'RESB':
        try:
            return int(operand)
        except:
            return 0
    elif instruction == 'BYTE':
        if operand.startswith("C'") and operand.endswith("'"):
            return len(operand[2:-1])
        elif operand.startswith("X'") and operand.endswith("'"):
            return len(operand[2:-1]) // 2
        else:
            return 1
    elif instruction == 'WORD':
        return 3

    return instruction_size.get(instruction, 3)


def is_valid_instruction(instruction):
    """Check if the instruction is valid"""
    instruction = instruction.upper()
    
    # Check if it's a format 4 instruction (starts with +)
    if instruction.startswith('+'):
        base_instruction = instruction[1:]
        return base_instruction in instruction_size
    
    # Check for format 4L instructions
    format4L_instructions = ['LITLD', 'LITAD', 'LITSB', 'LITCMP']
    if instruction in format4L_instructions:
        return True

    return instruction in instruction_size


def pass1(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    intermediate = []
    location_counter = []
    loc = 0
    invalid_instructions = []  # Track invalid instructions for reporting

    for line_num, line in enumerate(lines, 1):
        original_line = line.strip()  # Keep original line for error reporting
        line = line.strip()

        if ';' in line:
            line = line.split(';')[0].strip()  # Remove comments
        if not line:
            continue

        tokens = line.split()

        # Skip line numbers if present
        if tokens and tokens[0].isdigit():
            tokens = tokens[1:]  # Remove line number if present

        # Parse the line into label, instruction, and operand
        label, instruction, operand = '', '', ''
        if len(tokens) == 3:
            label, instruction, operand = tokens
        elif len(tokens) == 2:
            # Check if the first token is likely an instruction
            if is_valid_instruction(tokens[0]):
                instruction, operand = tokens
            else:
                label, instruction = tokens
        elif len(tokens) == 1:
            instruction = tokens[0]

        instruction = instruction.upper()

        # Check if the instruction is valid
        if not is_valid_instruction(instruction) and instruction not in ['START', 'END']:
            invalid_instructions.append((line_num, original_line, instruction))
            print(f"Error at line {line_num}: Invalid instruction '{instruction}'")
            continue  # Skip this line and don't include it in intermediate file

        if instruction == 'START':
            try:
                loc = int(operand, 16)
            except:
                loc = 0
            location = loc
            if label and label.upper() not in instruction_size:
                symbol_table[label] = f'{location:04X}'
        else:
            location = loc
            if label and label.upper() not in instruction_size:
                if label in symbol_table:
                    print(f"Error: Duplicate symbol '{label}'")
                else:
                    symbol_table[label] = f'{location:04X}'

        # Save intermediate representation and LC
        intermediate.append(f'{label}\t{instruction}\t{operand}'.strip())
        location_counter.append(f'{location:04X}')

        loc += get_size(instruction, operand)

    # Report summary of invalid instructions
    if invalid_instructions:
        print(f"\nFound {len(invalid_instructions)} invalid instructions:")
        for line_num, line, instruction in invalid_instructions:
            print(f"Line {line_num}: '{instruction}' in '{line}'")

    with open('data/intermediate.txt', 'w', encoding='utf-8') as f:
        for line in intermediate:
            f.write(line + '\n')

    with open('data/out_pass1.txt', 'w', encoding='utf-8') as f:
        for lc in location_counter:
            f.write(lc + '\n')

    with open('data/symbTable.txt', 'w', encoding='utf-8') as f:
        for symbol, addr in symbol_table.items():
            f.write(f'{symbol}\t{addr}\n')


if __name__ == "__main__":
    pass1('data/in.txt')