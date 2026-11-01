import gzip
import re
import urllib.request
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration & List URLs
# ---------------------------------------------------------------------------
BLOCKLIST_URLS = [
    "https://big.oisd.nl/",
    "https://easylist.to/easylist/easylist.txt",
    "https://easylist.to/easylist/easyprivacy.txt",
    "https://easylist.to/easylist/fanboy-social.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/dga7.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/doh-vpn-proxy-bypass.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/dyndns.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/fake.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.huawei.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.lgwebos.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.oppo-realme.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.roku.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.samsung.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.tiktok.extended.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.vivo.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/native.xiaomi.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/pro.plus.txt",
    "https://hagezi-mirror.dnsbunker.org/adblock/tif.txt",
    "https://perflyst.github.io/PiHoleBlocklist/AmazonFireTV.txt",
    "https://perflyst.github.io/PiHoleBlocklist/android-tracking.txt",
    "https://perflyst.github.io/PiHoleBlocklist/regex.list",
    "https://perflyst.github.io/PiHoleBlocklist/SessionReplay.txt",
    "https://perflyst.github.io/PiHoleBlocklist/SmartTV.txt",
    "https://perflyst.github.io/PiHoleBlocklist/SmartTV-AGH.txt",
    "https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt",
    "https://raw.githubusercontent.com/ftpmorph/ftpihole/master/blocklists/xiaomi-ads-tracking.txt",
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts",
    "https://raw.githubusercontent.com/unknownFalleN/xiaomi-dns-blocklist/master/xiaomi_dns_block.lst",
    "https://secure.fanboy.co.nz/fanboy-annoyance.txt",
    "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt",
    "https://v.firebog.net/hosts/Easylist.txt",
]

DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def clean_line(line):
    line = line.strip()
    if not line or line.startswith(("#", "!", ";")):
        return None

    # Handle standard hosts format (0.0.0.0 domain or 127.0.0.1 domain)
    parts = line.split()
    if len(parts) >= 2 and parts[0] in ("0.0.0.0", "127.0.0.1"):
        domain = parts[1].strip()
    else:
        # Handle ABP syntax (||domain.com^)
        domain = line
        if domain.startswith("||"):
            domain = domain[2:]
        if "^" in domain:
            domain = domain.split("^")[0]

    domain = domain.lower().strip()
    if DOMAIN_REGEX.match(domain):
        return domain
    return None


def main():
    start_dt = datetime.now()
    hagezi_domains = set()
    general_domains = set()

    for url in BLOCKLIST_URLS:
        print(f"Fetching: {url}")
        is_hagezi = "hagezi" in url.lower()
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "PiHole-Aggregator/1.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode("utf-8", errors="ignore")
                parsed_count = 0
                for line in content.splitlines():
                    domain = clean_line(line)
                    if domain:
                        if is_hagezi:
                            hagezi_domains.add(domain)
                        else:
                            general_domains.add(domain)
                        parsed_count += 1
                print(f"  -> Extracted {parsed_count:,} domains.")
        except Exception as e:
            print(f"  -> ERROR fetching {url}: {e}")
            
    # Deduplicate non-HaGeZi lists against HaGeZi lists so general.txt has ZERO overlap
    general_domains = general_domains - hagezi_domains
    
    # Write HaGeZi List
    hagezi_sorted = sorted(list(hagezi_domains))
    print(
        f"\nWriting {len(hagezi_sorted):,} unique domains to hagezi.txt..."
    )
    with open("hagezi.txt", "w", encoding="utf-8") as f:
        f.write("# Collated HaGeZi Blocklist\n")
        f.write(f"# Generated on: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Unique domains: {len(hagezi_sorted):,}\n\n")
        for domain in hagezi_sorted:
            f.write(f"{domain}\n")

    # Write General/Other List
    general_sorted = sorted(list(general_domains))
    print(
        f"Writing {len(general_sorted):,} unique domains to general.txt..."
    )
    with open("general.txt", "w", encoding="utf-8") as f:
        f.write("# Collated General & Niche Blocklists (OISD, Perflyst, etc.)\n")
        f.write(f"# Generated on: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Unique domains: {len(general_sorted):,}\n\n")
        for domain in general_sorted:
            f.write(f"{domain}\n")


if __name__ == "__main__":
    main()
