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

symbol_table = {}

def get_size(instruction, operand):
    instruction = instruction.upper()

    if instruction.startswith('+'):
        base_instruction = instruction[1:].upper()
        if base_instruction in instruction_size:
            return 4
        return 3

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

    for line in lines:
        line = line.strip()

        if ';' in line:
            line = line.split(';')[0].strip()  # Remove comments
        if not line:
            continue

        tokens = line.split()

        if tokens and tokens[0].isdigit():
            tokens = tokens[1:]

        label, instruction, operand = '', '', ''
        if len(tokens) == 3:
            label, instruction, operand = tokens
        elif len(tokens) == 2:
            # Check if the first token is an instruction
            if tokens[0].upper() in instruction_size or tokens[0].startswith('+'):
                instruction, operand = tokens
            else:
                label, instruction = tokens
        elif len(tokens) == 1:
            instruction = tokens[0]

        instruction = instruction.upper()

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

    with open('intermediate.txt', 'w', encoding='utf-8') as f:
        for line in intermediate:
            f.write(line + '\n')

    with open('out_pass1.txt', 'w', encoding='utf-8') as f:
        for lc in location_counter:
            f.write(lc + '\n')

    with open('symbTable.txt', 'w', encoding='utf-8') as f:
        for symbol, addr in symbol_table.items():
            f.write(f'{symbol}\t{addr}\n')


if __name__ == "__main__":
    pass1('in.txt')