import subprocess

def get_wifi_passwords():
    """
    Retrieves and displays saved Wi-Fi networks and their passwords on a Windows machine.
    Only displays networks that have a saved password.
    """
    try:
        # Execute netsh command to get all Wi-Fi profiles
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
    except Exception as e:
        print(f"Error: Unable to fetch Wi-Fi profiles. Exception: {e}")
        return

    # Extract Wi-Fi profile names from the command output
    # Profile names are listed after "All User Profile : "
    profile_names = [line.split(":")[1].strip() for line in data if "All User Profile" in line]
    
    wifi_data = []
    
    for name in profile_names:
        try:
            # For each profile, run netsh to get the security key in clear text
            detail_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
            
            # Look for the "Key Content" line which contains the actual password
            passwords = [line.split(":")[1].strip() for line in detail_output if "Key Content" in line]
            
            # Store only if a password was found (ignore open/unsecured networks)
            if passwords:
                wifi_data.append({"network": name, "password": passwords[0]})
        except Exception:
            # Skip any profiles that encounter errors during data extraction
            continue

    # Sort the list of networks alphabetically for better readability
    wifi_data.sort(key=lambda x: x['network'].lower())

    # Display the results in a clean, professional table format
    if not wifi_data:
        print("\n[!] No secured Wi-Fi networks with saved passwords were found.\n")
        return

    print("\n" + "="*70)
    print(f"{'Wi-Fi Network Name':<40} | {'Password':<25}")
    print("-" * 70)

    for item in wifi_data:
        network = item['network']
        password = item['password']
        print(f"{network:<40} | {password:<25}")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    get_wifi_passwords()
