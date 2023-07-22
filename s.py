import argparse

def print_string(domain):
    subdomains = set()

    # Add common subdomains to check (e.g., www, mail, ftp, etc.)
    common_subdomains = ["www", "mail", "ftp", "admin", "blog", "api"]
    for subdomain in common_subdomains:
        subdomains.add(f"{subdomain}.{domain}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--print-string", type=str, help="Print the provided string.")
    args = parser.parse_args()

    if args.print_string:
        print_string(args.print_string)
    else:
        print("Error: Please provide the string using the -d flag.")
