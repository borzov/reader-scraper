"""
ReaderScraper: Автоматизированная агрегация контента по доменам из веб-URL
-----------------------------------------------------------------------
Автор: Максим Борзов

Описание:
Этот скрипт автоматизирует получение веб-контента с использованием Jina AI Reader API.
Он обрабатывает URL из файла, сохраняет контент в папки, специфичные для доменов,
и генерирует файл с резюме в каждой папке. Скрипт поддерживает опциональную команду для
суммирования контента по доменам.

Использование:
-   Чтобы обработать URL из 'url.txt' и сохранить в папки, специфичные для доменов:
  $ python3 main.py

-   Чтобы создать файл с резюме для всего контента в определенной папке:
  $ python3 main.py --summarize [опционально: имя папки]
"""

import os
import sys
import argparse
import time
import logging
from urllib.parse import urlparse
from tqdm import tqdm
import asyncio
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_content(session, reader_url, site_url):
    """Асинхронное получение контента с помощью Reader API для заданного URL."""
    try:
        async with session.get(f'{reader_url}{site_url}') as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.error(f"Ошибка при получении {site_url}: {response.status}")
                return None
    except Exception as e:
        logging.error(f"Исключение при получении {site_url}: {e}")
        return None

def extract_title(content):
    """Извлечение заголовка из контента на основе первой строки."""
    first_line = content.split('\n')[0]
    return first_line[7:].strip() if first_line.startswith('Title: ') else "Unknown Title"

def summarize_contents(output_dir, domain):
    """Создание файла с резюме для домена в указанной директории."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    summary_file_name = f"!{domain}_summarize.txt"
    summary_file_path = os.path.join(output_dir, summary_file_name)
    with open(summary_file_path, 'w') as summary_file:
        summary_file.write(f"Сводка контента для {domain}:\n\n")
        for filename in sorted(os.listdir(output_dir)):
            if filename.endswith(".txt") and not filename.startswith("!"):
                path = os.path.join(output_dir, filename)
                with open(path, 'r') as content_file:
                    content = content_file.read()
                summary_file.write(f"Контент файла {filename}:\n<content>{content}</content>\n\n")

async def main():
    parser = argparse.ArgumentParser(description="Получение и суммирование веб-контента с организацией по доменам.")
    parser.add_argument('--summarize', action='store_true', help="Создать файл с резюме для всех содержимых в указанной папке.")
    args = parser.parse_args()

    reader_url = "https://r.jina.ai/"
    urls_filename = "url.txt"
    base_path = "scrape"
    processed_domains = set()
    start_time = time.time()

    if not os.path.exists(urls_filename):
        logging.error(f"Файл со списком URL '{urls_filename}' не найден.")
        return

    with open(urls_filename, 'r') as file:
        urls = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

    successful_requests = 0
    failed_requests = 0
    total_content_length = 0

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_content(session, reader_url, url))

        for url, content in zip(urls, await asyncio.gather(*tasks)):
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            domain_path = os.path.join(base_path, domain)
            if not os.path.exists(domain_path):
                os.makedirs(domain_path)
                logging.info(f"Создана директория `{domain_path}` для домена {domain}.")

            if content:
                successful_requests += 1
                title = extract_title(content)
                timestamp = int(time.time())
                filename = f"{timestamp}_{title}.txt"
                filepath = os.path.join(domain_path, filename)
                with open(filepath, 'w') as f:
                    f.write(content)
                total_content_length += len(content)
            else:
                failed_requests += 1

            processed_domains.add(domain)

    for domain in processed_domains:
        domain_path = os.path.join(base_path, domain)
        summarize_contents(domain_path, domain)

    time_elapsed = time.time() - start_time
    logging.info(f"Обработано {len(urls)} URL за {time_elapsed:.2f} секунд.")
    logging.info(f"Успешные запросы: {successful_requests}, Неудачные запросы: {failed_requests}")
    logging.info(f"Общая длина контента: {total_content_length} символов")

if __name__ == "__main__":
    asyncio.run(main())
