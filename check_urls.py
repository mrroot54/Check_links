import requests
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def check_link(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return (url, True, f"{Fore.GREEN}The link {url} is alive (status code: 200 OK).")
        else:
            return (url, False, f"{Fore.RED}The link {url} is dead (status code: {response.status_code}).")
    except requests.exceptions.RequestException as e:
        return (url, False, f"{Fore.RED}The link {url} is dead (Exception: {e}).")

def check_links_from_file(file_path, timeout):
    with open(file_path, 'r') as file:
        urls = [url.strip() for url in file if url.strip()]  # Read and strip URLs

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_link, url, timeout): url for url in urls}

        with open('200.txt', 'a') as output_file:
            for future in as_completed(futures):
                url, is_alive, result = future.result()
                print(result)
                if is_alive:
                    output_file.write(url + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check the status of URLs from a file and save URLs with a 200 status code to 200.txt.",
        usage="python %(prog)s [-t TIMEOUT] Path_Urls"
    )
    parser.add_argument("file_path", help="Path to the file containing URLs")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="Timeout for each URL request in seconds (default is 10 seconds)")

    args = parser.parse_args()
    file_path = args.file_path
    timeout = args.timeout

    check_links_from_file(file_path, timeout)
