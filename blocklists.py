from datetime import datetime
import glob
import gzip
import io
import os
import sys
import time
import urllib.request

# ==========================================
# CONFIGURATION
# ==========================================
BLOCKLIST_URLS = [
    (
        "https://raw.githubusercontent.com/ftpmorph/ftpihole/master/blocklists/xiaomi-ads-tracking.txt"
    ),
    (
        "https://raw.githubusercontent.com/unknownFalleN/xiaomi-dns-blocklist/master/xiaomi_dns_block.lst"
    ),
    "https://easylist.to/easylist/easylist.txt",
    "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://secure.fanboy.co.nz/fanboy-annoyance.txt",
    "https://easylist.to/easylist/fanboy-social.txt",
    "https://big.oisd.nl/",
    "https://v.firebog.net/hosts/Easylist.txt",
    (
        "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt"
    ),
    (
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts"
    ),
    "https://perflyst.github.io/PiHoleBlocklist/AmazonFireTV.txt",
    "https://perflyst.github.io/PiHoleBlocklist/SessionReplay.txt",
    "https://perflyst.github.io/PiHoleBlocklist/SmartTV-AGH.txt",
    "https://perflyst.github.io/PiHoleBlocklist/SmartTV.txt",
    "https://perflyst.github.io/PiHoleBlocklist/android-tracking.txt",
    "https://perflyst.github.io/PiHoleBlocklist/regex.list",
    "https://hagezi-mirror.dnsbunker.org/adblock/pro.plus.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/tif.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/dga30.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/dyndns.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/doh-vpn-proxy-bypass.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.tiktok.extended.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.huawei.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.samsung.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.lgwebos.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.roku.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.vivo.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.oppo-realme.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.xiaomi.txt",
]

LOCAL_FOLDER = None  # Optional: path to a folder with local blocklists
OUTPUT_FILE = "slimline_blocklist.txt"

# Robustness settings
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Logging settings
LOG_DIR = "./logs"
MAX_LOGS_TO_KEEP = 5


class Logger:
  """Helper class to write output simultaneously to the console and a log file."""

  def __init__(self, log_filepath):
    self.terminal = sys.stdout
    os.makedirs(os.path.dirname(log_filepath), exist_ok=True)
    self.log = open(log_filepath, "w", encoding="utf-8")

  def write(self, message):
    self.terminal.write(message)
    self.terminal.flush()
    self.log.write(message)
    self.log.flush()

  def flush(self):
    self.terminal.flush()
    self.log.flush()


def cleanup_old_logs(log_dir, max_keep=5):
  """Deletes old log files, keeping only the most recent N logs."""
  try:
    log_pattern = os.path.join(log_dir, "*_pihole_log.txt")
    log_files = sorted(glob.glob(log_pattern), key=os.path.getmtime)

    while len(log_files) > max_keep:
      old_file = log_files.pop(0)
      os.remove(old_file)
      print(f"[Cleanup] Removed old log file: {old_file}")
  except Exception as e:
    print(f"[Warning] Failed to cleanup old logs: {e}")


def parse_line(line):
  """Cleans a line and extracts the domain whether it's plain text or hosts format."""
  line = line.strip()

  if not line or line.startswith(("#", "!", ";", "[", "@")):
    return None

  parts = line.split()
  if not parts:
    return None

  if len(parts) >= 2 and (
      parts[0] in ("0.0.0.0", "127.0.0.1", "::1") or "." in parts[0]
  ):
    domain = parts[1]
  else:
    domain = parts[0]

  domain = domain.split("#")[0].strip()

  if "." in domain and not domain.startswith("."):
    if not all(part.isdigit() for part in domain.split(".")[-2:]):
      return domain.lower()

  return None


def fetch_from_url(url):
  """Downloads a blocklist from a URL sequentially with retries and timeout."""
  print(f"Fetching: {url}")
  domains = []
  raw_count = 0

  headers = {
      "User-Agent": "Mozilla/5.0 (Compatible; Pihole-Consolidator/2.0)",
      "Accept-Encoding": "gzip, deflate",
  }

  for attempt in range(1, MAX_RETRIES + 1):
    try:
      req = urllib.request.Request(url, headers=headers)
      with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
        content_encoding = response.headers.get("Content-Encoding", "")
        raw_data = response.read()

        if "gzip" in content_encoding or url.endswith(".gz"):
          try:
            decompressed_data = gzip.decompress(raw_data)
            text_stream = io.TextIOWrapper(
                io.BytesIO(decompressed_data), encoding="utf-8", errors="ignore"
            )
          except Exception:
            text_stream = io.TextIOWrapper(
                io.BytesIO(raw_data), encoding="utf-8", errors="ignore"
            )
        else:
          text_stream = io.TextIOWrapper(
              io.BytesIO(raw_data), encoding="utf-8", errors="ignore"
          )

        for line in text_stream:
          raw_count += 1
          domain = parse_line(line)
          if domain:
            domains.append(domain)

        print(
            f"  -> SUCCESS: Extracted {len(domains):,} valid domains (out of"
            f" {raw_count:,} raw lines) from {url.split('//')[-1]}"
        )
        return domains

    except Exception as e:
      print(f"  -> WARNING: Attempt {attempt}/{MAX_RETRIES} failed for {url}: {e}")
      if attempt < MAX_RETRIES:
        print(f"  -> Retrying in {RETRY_DELAY} seconds...")
        time.sleep(RETRY_DELAY)
      else:
        print(
            f"  -> ERROR: Failed to fetch {url} after {MAX_RETRIES} attempts."
        )

  return domains


def read_from_file(filepath):
  """Reads a local blocklist file, supporting standard or .gz compression."""
  print(f"Reading local file: {filepath}")
  domains = []
  raw_count = 0
  try:
    open_func = gzip.open if filepath.endswith(".gz") else open
    with open_func(filepath, "rt", encoding="utf-8", errors="ignore") as f:
      for line in f:
        raw_count += 1
        domain = parse_line(line)
        if domain:
          domains.append(domain)
    print(
        f"  -> SUCCESS: Extracted {len(domains):,} valid domains (out of"
        f" {raw_count:,} raw lines) from local file."
    )
  except Exception as e:
    print(f"  -> ERROR: Error reading {filepath}: {e}")
  return domains


def main():
  start_dt = datetime.now()
  timestamp_str = start_dt.strftime("%Y-%m-%d_%H-%M-%S")
  log_filename = f"{timestamp_str}_pihole_log.txt"
  log_filepath = os.path.join(LOG_DIR, log_filename)

  sys.stdout = Logger(log_filepath)

  try:
    all_domains_list = []

    print("==================================================")
    print(f"Pi-hole Blocklist Consolidation Started")
    print(f"Start Time : {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print("==================================================")

    # 1. Fetch from URLs sequentially
    if BLOCKLIST_URLS:
      print(
          f"\n--- Processing {len(BLOCKLIST_URLS)} Remote URL(s) Sequentially"
          " ---"
      )
      for url in BLOCKLIST_URLS:
        all_domains_list.extend(fetch_from_url(url))

    # 2. Read from local folder if provided
    if LOCAL_FOLDER and os.path.isdir(LOCAL_FOLDER):
      print(f"\n--- Processing Local Folder: {LOCAL_FOLDER} ---")
      for filename in os.listdir(LOCAL_FOLDER):
        filepath = os.path.join(LOCAL_FOLDER, filename)
        if os.path.isfile(filepath):
          all_domains_list.extend(read_from_file(filepath))

    if not all_domains_list:
      print(
          "\n[!] ERROR: No domains collected from any source. Aborting write."
      )
      return

    total_parsed_before_dedup = len(all_domains_list)

    # Deduplicate by converting to a set, then sort alphabetically
    print("\nDeduplicating and sorting domains...")
    unique_domains = sorted(list(set(all_domains_list)))
    total_unique = len(unique_domains)
    duplicates_removed = total_parsed_before_dedup - total_unique

    # 3. Write out the slimline list
    print(f"Writing {total_unique:,} unique domains to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
      f.write("# Collated Pi-hole Slimline Blocklist\n")
      f.write(f"# Generated on: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
      f.write(f"# Total raw domains parsed: {total_parsed_before_dedup:,}\n")
      f.write(f"# Duplicates removed: {duplicates_removed:,}\n")
      f.write(f"# Final unique domains: {total_unique:,}\n\n")
      for domain in unique_domains:
        f.write(f"{domain}\n")

    end_dt = datetime.now()
    elapsed = (end_dt - start_dt).total_seconds()

    print("==================================================")
    print(f"SUCCESS: Consolidation Finished")
    print(f"Start Time             : {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End Time               : {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Duration         : {elapsed:.2f} seconds")
    print(f"Total Raw Domains Parsed : {total_parsed_before_dedup:,}")
    print(f"Duplicates Removed       : {duplicates_removed:,}")
    print(f"Final Unique Domains     : {total_unique:,}")
    print("==================================================")

  finally:
    cleanup_old_logs(LOG_DIR, MAX_LOGS_TO_KEEP)


if __name__ == "__main__":
  main()
