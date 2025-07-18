import requests
import re

BASE_RAW = "https://raw.githubusercontent.com/mikepierce/internet-radio-streams/main/"

# List of all .m3u filenames in the repo
FILES = [
    "313.FM.m3u", "9128.live.m3u", "AM-Ambient.m3u", "AfterhoursFM.m3u",
    "AmbientSleepingPill.m3u", "BBC-WorldService.m3u", "BadRadio.m3u",
    "Bluemars.m3u", "CashmereRadio.m3u", "DandelionRadio.m3u",
    "DarkAmbientRadio.m3u", "DialRadio.m3u", "Dogglounge.m3u",
    "Dublab.m3u", "FIP-Stations.m3u", "Frisky.m3u", "Hirschmilch-Stations.m3u",
    "KCHUNG.m3u", "KEXP-Seattle.m3u", "KRCC-CO-Public.m3u", "KSPC-Claremont.m3u",
    "KXLU-SoCalLoyolaMarymount.m3u", "KioskRadio.m3u", "LeMellotron.m3u",
    "NASA-ThirdRockRadio.m3u", "NTS1.m3u", "NTS2.m3u", "Nectarine.m3u",
    "NewtownRadio.m3u", "NightwavePlaza.m3u", "RadioCaroline.m3u",
    "RadioParadise-Global.m3u", "RadioParadise-MainMix.m3u", "RadioRivendell.m3u",
    "Radiomeuh.m3u", "RePlayScrape.m3u", "RinseFM.m3u", "SanctuaryRadio.m3u",
    "ShonenBeachFM.m3u", "Slay-Radio.m3u", "SleepbotEnvironmental.m3u",
    "Sleepscapes-Rain.m3u", "Sleepscapes-Waves.m3u", "SohoRadio.m3u",
    "SomaFM-DeepSpaceOne.m3u", "SomaFM-DroneZone.m3u", "SomaFM-GrooveSalad.m3u",
    "SomaFM-IllinoisStreetLounge.m3u", "SomaFM-Lush.m3u", "SomaFM-SF10-33.m3u",
    "SomaFM-SpaceStation.m3u", "Subcity.m3u", "SyntheticFM-Synth.m3u",
    "TheLotRadio.m3u", "WorldwideFM.m3u"
]

def extract_url_from_m3u(text):
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None

def fetch_all_streams():
    urls = []
    for fname in FILES:
        raw_url = BASE_RAW + fname
        resp = requests.get(raw_url)
        if resp.status_code == 200:
            extracted = extract_url_from_m3u(resp.text)
            urls.append(extracted)
            print(".", end="")
        else:
            print(f"Warning: failed to fetch {fname} (HTTP {resp.status_code})")
    return urls

if __name__ == "__main__":
    streams = fetch_all_streams()
    output_file = "streams.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Found {len(streams)} stream URLs\n")
        for u in streams:
            f.write(f"'{u}',\n")

    print(f"Saved {len(streams)} stream URLs to '{output_file}'")

