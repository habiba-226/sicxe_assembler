from src.instructions import instruction_size

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