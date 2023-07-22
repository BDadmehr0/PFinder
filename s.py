import socket

def get_subdomains(domain):
    subdomains = set()

    # Add common subdomains to check (e.g., www, mail, ftp, etc.)
    common_subdomains = ["www", "mail", "ftp", "admin", "blog", "api"]
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
    domain_to_check = "rirabook.com"
    subdomains = get_subdomains(domain_to_check)
    print(f"Subdomains of {domain_to_check}:")
    for subdomain in subdomains:
        print(subdomain)

