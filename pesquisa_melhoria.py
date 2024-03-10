import requests
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urljoin

def get_links_from_site(site_url):
    response = requests.get(site_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a', href=True)
    return [urljoin(site_url, link['href']) for link in links]

def filter_links(links, keywords):
    return [link for link in links if any(keyword.lower() in link.lower() for keyword in keywords)]

def save_links_to_db(links):
    conn = sqlite3.connect('pesquisa_melhoria.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS links
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      url TEXT)''')

    for link in links:
        cursor.execute("SELECT * FROM links WHERE url=?", (link,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO links (url) VALUES (?)", (link,))
            print(f"Link salvo no banco de dados: {link}")

    conn.commit()
    conn.close()

def main():
    # Lista de sites para pesquisar
    sites = [
        'https://g1.globo.com/',
        'https://www.cnnbrasil.com.br/',
        'https://www.estadao.com.br/',
        # Adicione mais sites aqui
    ]

    # Palavras-chave a serem pesquisadas nos links
    keywords = ['carro', 'morte', 'biden']

    # Obtém todos os links dos sites e filtra os links que contêm uma das palavras-chave
    filtered_links = []
    for site in sites:
        links_from_site = get_links_from_site(site)
        filtered_links.extend(filter_links(links_from_site, keywords))

    # Salva os links filtrados no banco de dados
    save_links_to_db(filtered_links)

if __name__ == "__main__":
    main()


# As palavras q lembro de pronto são:
# Noroeste
# Pampulha
# 34° BPM
# 34 BPM
# Belo Horizonte e Homicídio
# UFMG
# PUC
# Mineirão
# Mineirinho
# Anel Rodoviário
# 040
# SINDPPEN
# Saritur
# Viação Útil
# Aeroporto Carlos Prates

# Palavras de momento:

# Stock Car
# Confisco
# Pedreira Prado Lopes
# PPL
# Sumaré
# Nova Cachoeirinha
# Suvaco das Cobras
# Jardim São José
# Pindorama
# Castelo