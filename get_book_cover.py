import requests
from PIL import Image
from io import BytesIO

def get_book_thumbnail(title):
    # Search for the book by title
    search_url = f"https://openlibrary.org/search.json?title={title}"
    response = requests.get(search_url)
    response.raise_for_status()
    data = response.json()
    
    # If the book is found
    if data['docs']:
        # Get the first book's cover ID
        cover_id = data['docs'][0].get('cover_i')
        if cover_id:
            # Construct the cover URL
            cover_url = f"http://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            return cover_url
        else:
            return None
    else:
        return None

# Example usage
title = "The two towers"
thumbnail_url = get_book_thumbnail(title)

# show the thumbnail
if thumbnail_url:
    response = requests.get(thumbnail_url)
    response.raise_for_status()

    # convert to PIL image and show with external viewer
    image = Image.open(BytesIO(response.content))
    image.show()