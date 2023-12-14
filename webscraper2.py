import requests
from bs4 import BeautifulSoup
import re
import csv
url = "https://www.givewell.org/about/donate/cryptocurrency"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
content = soup.find_all('p')
content = str(content)

def find_crypto_wallets(text):

    eth_address_pattern = r'\b0x[a-fA-F0-9]{40}\b'
    btc_address_pattern = r'\b[13][a-km-zA-HJ-NP-Z0-9]{26,33}\b'
    sol_address_pattern = r'\b4[1-9A-HJ-NP-Za-km-z]{31,49}\b'
    xmr_address_pattern = r'\b(?:4|8)[0-9a-zA-Z]{75,}\b'

    
    combined_pattern = re.compile(f'{eth_address_pattern}|{btc_address_pattern}|{sol_address_pattern}|{xmr_address_pattern}')
    

    matches = re.findall(combined_pattern, text)
    
    wallet_info = []
    for match in matches:
        if re.match(eth_address_pattern, match):
            wallet_info.append(["ETH", match])
        elif re.match(btc_address_pattern, match):
            wallet_info.append(["BTC", match])
        elif re.match(sol_address_pattern, match):
            wallet_info.append(["SOL", match])
        elif re.match(xmr_address_pattern, match):
            wallet_info.append(["XMR", match])
    
    
    return wallet_info

crypto_wallets = find_crypto_wallets(content)

if crypto_wallets:
    print("Crypto Wallets found in the text:")
    for wallet_type, wallet_address in crypto_wallets:
        print(f"{wallet_type}: {wallet_address}")

    csv_filename = "crypto_wallets.csv"
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Wallet Type', 'Wallet Address'])
        csv_writer.writerows(crypto_wallets)
    print(f"\nWallet information exported to {csv_filename}")
else:
    print("No Crypto Wallets found in the text.")