
"""
SIC/XE Assembler Runner
"""
from src.assembler_pass1 import pass1
from src.assembler_pass2 import pass2

def main():

    input_file = 'data/in.txt'
    print(f"Running Pass 1 on {input_file}...")
    pass1(input_file)
    
    print("Running Pass 2...")
    pass2('data/intermediate.txt', 'data/out_pass1.txt', 'data/symbTable.txt')
    
    print("Assembly complete. Output files written to data directory.")

if __name__ == "__main__":
    main()