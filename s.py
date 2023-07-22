import argparse

def print_string(input_string):
    print(f"The string you entered is: {input_string}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--print-string", type=str, help="Print the provided string.")
    args = parser.parse_args()

    if args.print_string:
        print_string(args.print_string)
    else:
        print("Error: Please provide the string using the -d flag.")
