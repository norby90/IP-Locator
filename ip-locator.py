import requests
import sys

BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║ ██╗██████╗     ██╗      ██████╗  ██████╗ █████╗ ████████╗ ██████╗ ██████╗    ║ 
██║██╔══██╗      ██║     ██╔═══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗   ║ 
██║██████╔╝  ══  ██║     ██║   ██║██║     ███████║   ██║   ██║   ██║██████╔╝   ║ 
██║██╔═══╝   ══  ██║     ██║   ██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗   ║ 
██║██║           ███████╗╚██████╔╝╚██████╗██║  ██║   ██║   ╚██████╔╝██║  ██║   ║ 
╚═╝╚═╝           ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ║      
║Every device connected to the internet leaves a trace. This tool reads it     ║ 
║                                                                              ║ 
╚══════════════════════════════════════════════════════════════════════════════╝
"""

def get_ip_info(ip_address=None):
    """Fetch IP location information using ip-api.com"""
    if not ip_address:
        try:
            ip_address = requests.get("https://api.ipify.org?format=text", timeout=5).text
        except:
            return {"error": "Could not determine your IP address"}

    url = f"http://ip-api.com/json/{ip_address}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("status") == "success":
            return {
                "ip": data.get("query"),
                "country": data.get("country"),
                "country_code": data.get("countryCode"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "zip": data.get("zip"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "timezone": data.get("timezone"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "as": data.get("as")
            }
        else:
            return {"error": f"Invalid IP address: {ip_address}"}
    except Exception as e:
        return {"error": str(e)}

def display_info(info):
    print("\n" + "="*50)
    print("IP LOCATION INFORMATION")
    print("="*50)

    if "error" in info:
        print(f"\nError: {info['error']}")
        return

    fields = [
        ("IP Address", "ip"),
        ("Country", "country"),
        ("Country Code", "country_code"),
        ("Region", "region"),
        ("City", "city"),
        ("ZIP Code", "zip"),
        ("Latitude", "latitude"),
        ("Longitude", "longitude"),
        ("Timezone", "timezone"),
        ("ISP", "isp"),
        ("Organization", "org"),
        ("AS Number", "as")
    ]

    for label, key in fields:
        value = info.get(key, "N/A")
        print(f"{label:20}: {value}")

    print("="*50 + "\n")

def main():
    print("\033[1;91m" + BANNER + "\033[0m")
    if len(sys.argv) > 1:
        if sys.argv[1] == "-m" or sys.argv[1] == "--my-ip":
            print("\nFetching your IP information...")
            info = get_ip_info()
            display_info(info)
        else:
            ip = sys.argv[1]
            print(f"\nLooking up {ip}...")
            info = get_ip_info(ip)
            display_info(info)
    else:
        ip = input("Enter IP address: ").strip()
        if ip:
            print(f"\nLooking up {ip}...")
            info = get_ip_info(ip)
            display_info(info)
        else:
            print("No IP address entered.")

if __name__ == "__main__":
    main()
