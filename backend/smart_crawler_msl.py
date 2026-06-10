import os

def smart_crawl(index_file):
    if not os.path.exists(index_file):
        print("Error: msl_index.tab not found!")
        return

    with open(index_file, "r") as f:
        for line in f:
            # We look for the filename in the line
            # The filenames in PDS usually look like RME_...RMD...TAB
            parts = line.split(',')
            
            for part in parts:
                clean_name = part.strip().replace('"', '')
                
                # Filter for our three types
                if "RMD" in clean_name and clean_name.endswith(".TAB"):
                    print(f"[METEOROLOGICAL] Found: {clean_name}")
                elif "RNV" in clean_name and clean_name.endswith(".TAB"):
                    print(f"[WIND/NAV]       Found: {clean_name}")
                elif "ADR" in clean_name and clean_name.endswith(".TAB"):
                    print(f"[ANCILLARY]      Found: {clean_name}")

if __name__ == "__main__":
    smart_crawl("msl_index.tab")