import urllib.parse
import json
from pathlib import Path


def parse_carousell_url(url):
    special_params = ["&t-search_query_source=ss_dropdown",
                      "&t-search_query_source=direct_search"]

    if any(param in url for param in special_params):
        return {"full_url": url}

    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    path_parts = parsed_url.path.strip('/').split('/')

    if path_parts[0] == 'categories':
        # Join all parts after 'categories'
        category = '/'.join(path_parts[1:])
        search_query = query_params.get('search', [None])[0]
    else:
        category = None
        search_query = path_parts[1] if len(path_parts) > 1 else None

    sort_by = query_params.get('sort_by', ['3'])[
        0]  # Default to 3 if not present

    price_start = query_params.get('price_start', [None])[0]
    price_end = query_params.get('price_end', [None])[0]

    tab = query_params.get('tab', [None])[0]

    parsed_item = {
        "category": category,
        "query": search_query,
        "sort_by": int(sort_by),
        "price_start": int(price_start) if price_start else None,
        "price_end": int(price_end) if price_end else None,
        "tab": tab
    }

    # Check if all essential fields are parsed correctly
    if category and search_query:
        return parsed_item
    else:
        return {"full_url": url}


def add_search_item_from_url(config_file, url):
    search_item = parse_carousell_url(url)

    with open(config_file, 'r+') as f:
        config = json.load(f)
        if 'SEARCH_ITEMS' not in config:
            config['SEARCH_ITEMS'] = []
        config['SEARCH_ITEMS'].append(search_item)
        f.seek(0)
        json.dump(config, f, indent=2)
        f.truncate()

    return search_item


def main():
    config_file = Path(__file__).parent / 'config.json'

    print("Welcome to the Carousell Search URL Adder!")
    print("Please paste the Carousell search URL below:")

    url = input().strip()

    try:
        search_item = add_search_item_from_url(config_file, url)
        print("\nSearch item added successfully!")
        print("Details:")
        if "full_url" in search_item:
            print(f"full_url: {search_item['full_url']}")
            if "&t-search_query_source=ss_dropdown" in url:
                print(
                    "(Full URL was added due to presence of 't-search_query_source=ss_dropdown')")
            elif "&t-search_query_source=direct_search" in url:
                print(
                    "(Full URL was added due to presence of 't-search_query_source=direct_search')")
            else:
                print(
                    "(Full URL was added because the URL structure couldn't be fully parsed)")
        else:
            for key, value in search_item.items():
                print(f"{key}: {value}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Please make sure you've entered a valid Carousell search URL.")


if __name__ == "__main__":
    main()
