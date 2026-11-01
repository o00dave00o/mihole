# Pi-hole Slimline Blocklist Aggregator

An automated GitHub Actions workflow that fetches, cleans, deduplicates, and compresses multiple upstream blocklists into a single, highly optimized, gzipped blocklist (`blocklist.txt.gz`) for Pi-hole.

Designed to offload heavy lifting from resource-constrained local hardware (like older Raspberry Pi models) while maintaining a robust shield against trackers, malware, and telemetry.

---

## 🛠️ How It Works
1. **Automated Fetching:** Runs via GitHub Actions on a daily schedule to download lists sequentially.
2. **Parsing & Cleaning:** Strips comments, extracts bare domains from hosts/adblock formats, and filters out invalid entries.
3. **Deduplication:** Merges overlapping entries across all sources.
4. **Compression:** Outputs a gzipped file (`blocklist.txt.gz`) to stay well within GitHub storage limits while remaining natively readable by Pi-hole.

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

## 📥 How to Use in Pi-hole
If you want to use this aggregated list in your own Pi-hole:
1. Copy the **Raw** URL of the `blocklist.txt.gz` file from this repository.
2. In your Pi-hole Admin panel, go to **Adlists**.
3. Paste the URL and click **Add**.
