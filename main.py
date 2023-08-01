import argparse
import socket
import requests
import re

def check_url_status(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False            
    except requests.Timeout:
        return False
    except requests.RequestException as e:
        return False


# def validate_url(url):
#     # Regular expression pattern to match URLs
#     url_pattern = re.compile(
#         r'(?:[a-zA-Z0-9\-]+\.)*[a-zA-Z0-9\-]+'  # Domain (e.g., www.example.com)
#         r'(?:\.[a-zA-Z]{2,})'  # Top-level domain (e.g., .com, .org)
#         r'(?::\d+)?'  # Optional port number (e.g., :80)
#         r'(?:/[^\s]*)?$'  # Optional path (e.g., /page or /path/to/page)
#     )

#     # Check if the URL matches the pattern
#     return bool(url_pattern.match(url))



def finder(domain):
    subdomains = set()

    # Add common subdomains to check (e.g., www, mail, ftp, etc.)
    common_subdomains = ["www", "mail", "ftp", "admin", "blog", "api", "accounts", "adwords"]
    for subdomain in common_subdomains:
        subdomains.add(f"{subdomain}.{domain}")
    
    try:
        # Fetch DNS A records for the domain
        for record_type in ['A', 'CNAME']:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('8.8.8.8', 53))  # Use Google's public DNS server
                query = f"{domain} {record_type}\x00\x01"
                s.sendall(query.encode())

                data = s.recv(4096)
                while data:
                    # Parse DNS response to extract subdomains
                    index = data.find(query.encode())
                    if index == -1:
                        break

                    start = index + len(query) + 1
                    length = data[start]
                    subdomain = data[start + 1: start + 1 + length].decode()
                    subdomains.add(subdomain)

                    data = data[start + 1 + length:]
    except (socket.gaierror, ConnectionRefusedError, OSError):
        pass

    return subdomains

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--target-domain", type=str, help="Input Target domain.")
    args = parser.parse_args()


    if args.print_string:  # Corrected the attribute name here
        subdomains = finder(args.print_string)  # Corrected the attribute name here
        print(f"Subdomains of {args.print_string}:")
        for subdomain in subdomains:
            status = check_url_status(url="http://"+subdomain)
            print(f'{subdomain} status: {status}')
    else:
        print("Error: Please provide the string using the -d flag.")
