#!/usr/bin/env python3
import requests
import base64
import re
import os
import time
from pathlib import Path
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
import json

def decode_base64(encoded_str):
    """Decode base64 string"""
    return base64.b64decode(encoded_str).decode('utf-8')

def extract_sounds_from_html(html_content, base_url):
    """Extract sound information from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    sounds = []

    # Find all audio tags with src attribute
    audio_tags = soup.find_all('audio', src=True)

    for idx, audio in enumerate(audio_tags, 1):
        src = audio.get('src')

        # Remove leading slash and decode base64
        encoded_path = src.lstrip('/')
        try:
            decoded_path = decode_base64(encoded_path)
            full_url = urljoin(base_url, decoded_path)

            # Try to find the associated title
            # Look for the nearest blockquote or heading
            parent = audio.find_parent('div', class_='art-article')
            if parent:
                header = parent.find_previous('blockquote', class_='art-postheader')
                if header:
                    # Extract text without the number
                    title_text = header.get_text(strip=True)
                    # Remove the leading number
                    title_text = re.sub(r'^\d+\s+', '', title_text)
                else:
                    title_text = f"Sound {idx}"
            else:
                title_text = f"Sound {idx}"

            # Extract filename
            filename = decoded_path.split('/')[-1]

            sounds.append({
                'index': idx,
                'title': title_text,
                'url': full_url,
                'filename': filename
            })
        except Exception as e:
            print(f"Error decoding audio src: {src}, error: {e}")

    return sounds

def download_file(url, destination, session):
    """Download a file from URL to destination"""
    try:
        # Add delay to be polite
        time.sleep(2)

        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def get_audio_duration(filepath):
    """Try to get audio duration using ffprobe if available"""
    import subprocess
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', filepath],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return None

def main():
    base_url = "https://zonesons.com"
    base_page_url = "https://zonesons.com/repliques-cultes-de-films-d-espionnage/phrases-cultes-de-oss-117-le-caire-nid-d-espions/"

    # Total number of pages to download
    total_pages = 96

    # Create a session with browser-like headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })

    # Create sounds directory
    sounds_dir = Path("sounds")
    sounds_dir.mkdir(exist_ok=True)

    all_sounds = []
    downloaded_sounds = []
    global_index = 1

    print(f"Starting download of {total_pages} pages...")
    print("=" * 60)

    for page_num in range(1, total_pages + 1):
        # Construct page URL
        if page_num == 1:
            page_url = base_page_url
        else:
            page_url = f"{base_page_url}page-{page_num}#navtop"

        print(f"\n[Page {page_num}/{total_pages}] Fetching {page_url}...")

        try:
            # Add delay between page fetches to be respectful
            if page_num > 1:
                time.sleep(3)

            response = session.get(page_url, timeout=30)
            response.raise_for_status()

            # Extract sounds from the page
            page_sounds = extract_sounds_from_html(response.text, base_url)

            if not page_sounds:
                print(f"  ⚠️  No sounds found on page {page_num}")
                continue

            print(f"  Found {len(page_sounds)} sounds on page {page_num}")

            # Download sounds from this page
            for sound in page_sounds:
                print(f"  [{global_index}] Downloading: {sound['title'][:60]}...")

                # Create unique filename if needed
                destination = sounds_dir / sound['filename']

                # If file already exists, skip it
                if destination.exists():
                    print(f"    ⏭️  File already exists, skipping")
                    file_size = destination.stat().st_size
                    duration = get_audio_duration(str(destination))

                    downloaded_sounds.append({
                        'index': global_index,
                        'title': sound['title'],
                        'filename': sound['filename'],
                        'url': sound['url'],
                        'size': file_size,
                        'duration': duration
                    })
                    global_index += 1
                    continue

                if download_file(sound['url'], destination, session):
                    # Get file size
                    file_size = destination.stat().st_size

                    # Try to get duration
                    duration = get_audio_duration(str(destination))

                    downloaded_sounds.append({
                        'index': global_index,
                        'title': sound['title'],
                        'filename': sound['filename'],
                        'url': sound['url'],
                        'size': file_size,
                        'duration': duration
                    })
                    print(f"    ✓ Downloaded ({file_size} bytes, {duration:.1f}s)")
                else:
                    print(f"    ✗ Failed to download")

                global_index += 1

                # Save metadata after each sound (in case of interruption)
                metadata_file = sounds_dir / "metadata.json"
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(downloaded_sounds, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"  ✗ Error processing page {page_num}: {e}")
            continue

    print("\n" + "=" * 60)
    print(f"✅ DOWNLOAD COMPLETE!")
    print(f"✓ Downloaded {len(downloaded_sounds)} sounds to {sounds_dir}/")
    print(f"✓ Metadata saved to {sounds_dir}/metadata.json")

    # Calculate total statistics
    total_size = sum(s['size'] for s in downloaded_sounds)
    total_duration = sum(s.get('duration', 0) for s in downloaded_sounds if s.get('duration'))

    print(f"\n📊 Statistics:")
    print(f"   Total sounds: {len(downloaded_sounds)}")
    print(f"   Total size: {total_size / (1024*1024):.2f} MB")
    print(f"   Total duration: {int(total_duration // 60)}m {int(total_duration % 60)}s")

    return downloaded_sounds

if __name__ == "__main__":
    main()
