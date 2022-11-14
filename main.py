import requests
import json
import random
import webbrowser

def main():
    # ask user for a dateBegin and dateEnd
    dateBegin = input("Enter a start year (- for B.C.) (or nothing to continue): ")
    dateEnd = input("Enter an end year (- for B.C.)  (or nothing to continue): ")
    date = "" if (dateBegin == "" or dateEnd == "") else f'dateBegin={dateBegin}&dateEnd={dateEnd}'
    # ask user for mediums (separated by vertical bars)
    print("Enter mediums: Paintings, Sculpture, Drawing, Print or others")
    print("Separate mediums with vertical bars (|)")
    print("Example: Paintings|Sculpture|Drawing")
    mediums = input("Enter mediums: (or nothing to continue) ")
    mediums = mediums.split("|")
    mediums = [medium.lower() for medium in mediums]
    mediums = [medium.strip() for medium in mediums]
    mediums = [medium.title() for medium in mediums]
    mediums = "|".join(mediums)
    mediums = "" if mediums == "" else f'medium={mediums}'
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?{date}&{mediums}&hasImages=true&q=\"\""
    print(url)
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    if response.status_code != 200:
        print("Error: Could not get data")
        return
    data = response.json()
    if data["total"] == 0:
        print("No results found")
        return
    artworks = data["objectIDs"]
    random_artwork = random.choice(artworks)
    artwork_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{random_artwork}"
    artwork_response = requests.get(artwork_url)
    print(f"Artwork response: {artwork_response.status_code}")
    if artwork_response.status_code != 200:
        print("Error: Could not get data")
        return
    artwork_data = artwork_response.json()
    open = input("Open in browser? (y/n): ")
    if open == "y":
        webbrowser.open(artwork_data["objectURL"])
    else:
        # print all the data
        print(json.dumps(artwork_data, indent=4))
    

if __name__ == "__main__":
    main()