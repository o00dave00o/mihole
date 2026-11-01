# Pi-hole Blocklist Aggregator

An automated GitHub Actions workflow that fetches, cleans, deduplicates, and splits multiple upstream blocklists into two cleanly organized, uncompressed plain-text files (`hagezi.txt` and `general.txt`) for Pi-hole.

Designed to offload heavy lifting from resource-constrained local hardware (like older Raspberry Pi models) while maintaining a powerhouse shield against trackers, malware, and telemetry (specifically optimized for smart TVs, Fire Sticks, and IoT devices).

---

## 🛠️ How It Works

1. **Automated Fetching:** Runs via GitHub Actions on a schedule to download 31 distinct upstream feeds sequentially.
2. **Parsing & Cleaning:** Strips comments, metadata, and non-domain noise, extracting bare domains from hosts/adblock syntax and validating them against strict regex rules.
3. **Smart Deduplication & Logical Split:** 
   - Merges and deduplicates entries within HaGeZi feeds into `hagezi.txt`.
   - Merges all other feeds into `general.txt`.
   - Subtracts `hagezi.txt` domains from `general.txt` so there is **zero cross-file redundancy**.
4. **GitHub & Pi-hole Optimized:** Outputs two clean plain-text files to stay safely under GitHub's 100 MB file limit while allowing Pi-hole to read the records cleanly while leveraging on-the-fly HTTP `gzip` transport compression.

---

## 📥 How to Use in Pi-hole

To use these aggregated lists in your Pi-hole:

1. Open your **Pi-hole Admin Panel** and navigate to **Adlists**.
2. Add both of the following Raw URLs:
   ```text
   https://raw.githubusercontent.com/o00dave00o/mihole/main/hagezi.txt
   
   https://raw.githubusercontent.com/o00dave00o/mihole/main/general.txt

---

## 🙏 Credits & Upstream Sources
This repository does not create or maintain these blocklists. It merely aggregates and unifies them for personal use. Massive thanks to the incredible maintainers who curate these feeds:

### Core & General Blocklists
* **[OISD (Big)](https://oisd.nl/)** – Comprehensive, smart-filtering global blocklist.
* **[StevenBlack Hosts (Fakenews & Gambling)](https://github.com/StevenBlack/hosts)** – Unified hosts file variant targeting fake news and gambling networks.
* **[Firebog (Easylist Mirror)](https://firebog.net/)** – Curated baseline tracking lists.

### HaGeZi's DNS Blocklists ([GitHub Repository](https://github.com/hagezi/dns-blocklists))
* **Pro Plus (`pro.plus.txt`)** – Multi-tier threat intelligence and advanced protection.
* **Threat Intelligence Feeds (`tif.txt`)** – High-security malicious domain blocking.
* **Fake/Scam Protection (`fake.txt`)** – Anti-scam and deceptive site filters.
* **NRD Protection (`dga30.txt`)** – Newly registered domain filters.
* **DoH/VPN/Proxy Bypass (`doh-vpn-proxy-bypass.txt`)** – Prevents circumvention of filtering.
* **Dynamic DNS (`dyndns.txt`)** – Blocks dynamic DNS providers often abused by telemetry.
* **Native Device Telemetry Filters:**
  * Huawei (`native.huawei.txt`)
  * LG WebOS (`native.lgwebos.txt`)
  * Oppo / Realme (`native.oppo-realme.txt`)
  * Roku (`native.roku.txt`)
  * Samsung (`native.samsung.txt`)
  * TikTok Extended (`native.tiktok.extended.txt`)
  * Vivo (`native.vivo.txt`)
  * Xiaomi (`native.xiaomi.txt`)

### EasyList & Fanboy Filters ([Official Website](https://easylist.to/))
* **EasyList** – Premier list for blocking advertisements.
* **EasyPrivacy** – Comprehensive privacy tracking protection.
* **Fanboy Annoyances & Social** – Blocks page annoyances, widgets, and social media hooks.
* **Fanboy Cookie Monster & Cookie Lists** – Mitigates cookie consent pop-ups and tracking scripts.

### Perflyst's Pi-Hole Blocklists ([GitHub Repository](https://github.com/perflyst/PiHoleBlocklist))
* **Amazon Fire TV** – Tailored telemetry and metrics blocking for Fire devices.
* **Android Tracking** – Cross-app mobile telemetry mitigation.
* **SmartTV & SmartTV-AGH** – General smart-device telemetry and ad blocks.
* **Session Replay** – Blocks user-session recording and heatmapping trackers.
* **Regex List** – Advanced pattern-matching block rules.

### Specialized & Community Sources
* **[Windows Spy Blocker](https://github.com/crazy-max/WindowsSpyBlocker)** – Telemetry and spyware mitigation for Windows ecosystems.
* **Xiaomi Tracking Feeds** – Community-maintained lists for Xiaomi smart-device telemetry:
  * [ftpmorph's Xiaomi Ads Tracking](https://github.com/ftpmorph/ftpihole)
  * [unknownFalleN's Xiaomi DNS Blocklist](https://github.com/unknownFalleN/xiaomi-dns-blocklist)

---

