import requests
from bs4 import BeautifulSoup
import argparse
import subprocess
import os
import re
from colorama import Fore, Style
from tqdm import tqdm
import time

# Função para fazer a solicitação HTTP e extrair os resultados da pesquisa
def search_google(site, text):
    # Lista para armazenar URLs únicas
    unique_urls = []

    # Realizar a pesquisa nas páginas 1, 2 e 3
    for page in range(1, 2):
        # Construindo a URL de pesquisa do Google com base nos argumentos fornecidos
        url = f'https://www.google.com/search?q=site%3A"{site}"%20inurl%3Awp-content%2F%20intext%3A{text}&start={page * 10}'

        # Fazendo a solicitação HTTP e obtendo o conteúdo da página
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Procurando pelos links dos resultados da pesquisa
        search_results = soup.find_all('a')

        # Armazenar as URLs únicas encontradas
        for result in search_results:
            url = result['href']
            if url.startswith('/url?q='):
                url = url[7:]
                url = url.split('wp-content')[0]  # Remover tudo após "wp-content"
                if 'google' not in url:  # Ignorar URLs com "google"
                    if url not in unique_urls:  # Verificar se a URL já foi adicionada
                        unique_urls.append(url)

        # Aguardar por alguns segundos antes de fazer a próxima solicitação
        time.sleep(2)

    # Imprimir a mensagem de escaneamento
    print(Fore.GREEN + "\nEscaneando sites..." + Style.RESET_ALL)

    # Dicionário para armazenar os emails únicos encontrados agrupados por URL
    emails_by_url = {}

    # Verificar a presença de emails em cada site da lista
    for site_url in tqdm(unique_urls, desc="Progresso", unit="site"):
        site_name = site_url.split('//')[1].split('/')[0]  # Extrair o nome do site do URL
        output_file = f'{site_name}.txt'  # Nome do arquivo de saída

        # Executar curl e salvar a saída no arquivo
        with open(output_file, 'w') as file:
            subprocess.run(['curl', '-s', site_url], stdout=file)

        # Procurar por emails no arquivo
        with open(output_file, 'r') as file:
            file_content = file.read()
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', file_content)
            count = 0
            for email in emails:
                if len(email) > 14 and count < 3 and not email.startswith('cached@'):
                    if email not in emails_by_url.setdefault(site_url, []):
                        emails_by_url[site_url].append(email)
                        count += 1

        # Remover o arquivo
        os.remove(output_file)

    # Imprimir os emails encontrados agrupados por URL
    if emails_by_url:
        print(Fore.BLUE + "\nSites com emails encontrados:" + Style.RESET_ALL)
        for site_url, emails in emails_by_url.items():
            print(f"\nURL: {site_url}")
            print(Fore.RED + "Emails:")
            for email in emails:
                print(email)
            print(Style.RESET_ALL)
            
    

    # Executar wpscan nos sites que possuem emails
    with tqdm(total=len(emails_by_url), desc="Progresso do wpscan", unit="site") as pbar:
        for site_url in emails_by_url.keys():
            site_name = site_url.split('//')[1].split('/')[0]  # Extrair o nome do site do URL
            output_file = f'{site_name}_report.txt'  # Nome do arquivo de saída

            print(Fore.GREEN + f"\nExecutando o wpscan no site {site_url}..." + Style.RESET_ALL)
            run_wpscan(site_url, output_file)
            pbar.update(1)


# Função para executar o comando wpscan e salvar o relatório em um arquivo de texto
def run_wpscan(site_url, output_file):
    wpscan_command = f"wpscan --url {site_url} --api-token {token} --enumerate vp --update --random-user-agent --ignore-main-redirect | grep -i '[!]\| url:\|started\|Aborted' | grep -v 'Effective\|style\|WARNING\|The version'"
    
    with tqdm(total=100, desc="Progresso do wpscan", unit="%", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        process = subprocess.Popen(wpscan_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, error = process.communicate()

        if process.returncode != 0:
            print(Fore.RED + "Ocorreu um erro ao executar o comando wpscan:")
            print(error)
            return

        # Salvar a saída do comando no arquivo de texto
        with open(output_file, 'w') as file:
            file.write(output)
            
# Token para o wpscan
token = "seu_token_aqui"


# Definindo os argumentos da linha de comando
parser = argparse.ArgumentParser(description='Web Scraper para buscar dork no Google.')
parser.add_argument('--site', help='Domínio do site (exemplo: br)', required=True)
parser.add_argument('--text', help='Texto a ser procurado (exemplo: escola)', required=True)
args = parser.parse_args()


# Chamando a função de busca do Google
search_google(args.site, args.text)
