import sys

def print_string(input_string):
    print(f"The string you entered is: {input_string}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Please provide one string argument.")
    else:
        input_string = sys.argv[1]
        print_string(input_string)
