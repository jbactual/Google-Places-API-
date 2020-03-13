import googlemaps

# Define google maps client
API_KEY = "AIzaSyDYBoNYYfvINm3c4Mn5nUMNC2-FJkOufPA"
gmaps = googlemaps.Client(key=API_KEY)

def remove_types(details):
    try: 
        detailTypes = []
        detailTypes = details['result']['types']
        del(details['result']['types'])

        detailTypes.remove('point_of_interest')
        detailTypes.remove('establishment')

        details['result']['types'] = detailTypes

        return details

    except:
        return details
        
        
# Defines initial search and provides 20 results
def first_request(bType, cityCoords):
    try: 
        result = gmaps.places_nearby(location=f"{cityCoords[0]},{cityCoords[1]}", radius=40000, open_now=False, type=f"{bType}")
        gmaps_result = result["results"]
        gmaps_token = result["next_page_token"]
        return gmaps_result, gmaps_token
    except:
        gmaps_token = False
        return gmaps_result, gmaps_token

def second_request(gmaps_token):
    try: 
        result = gmaps.places_nearby(page_token=f"{str(gmaps_token)}")
        gmaps_result = result["results"]
        gmaps_token = result["next_page_token"]
        return gmaps_result, gmaps_token
    except:
        gmaps_token = False
        return gmaps_result, gmaps_token
        

def third_request(gmaps_token):
    try: 
        result = gmaps.places_nearby(page_token=f"{str(gmaps_token)}")
        gmaps_result = result["results"]
        return gmaps_result
    except:
        gmaps_result = False
        return gmaps_result



def places_api(bType, cityCoords):

    # Sets fields to extract from google place api
    my_fields = ['name', 'formatted_address', 'website', 'type']
    
    # Creates dictionary to store values after request
    jsonData = {}
    jsonData[f"{bType}"] = []

    # Makes 3 requests per category or gets 60 results total
    # Cant request more than 60 for each coordinate
    for n in range(0, 3, 1):

        # Determines if it's an initial/secondary request
        # Initial and second request returns a page token
        # If you attempt to extract a token when none is provided
        # python throws an error
        if n == 0: 
            gmaps_result, gmaps_token = first_request(bType, cityCoords)
        elif n == 1 and gmaps_token != False:
            gmaps_result, gmaps_token = second_request(gmaps_token)
        elif n == 2 and gmaps_token != False: 
            gmaps_result = third_request(gmaps_token)
        else: 
            return


        # Sifts through gmaps data set, gets each placeId 
        # and requests specified fields from above
        # Then appends the data to the dictionary created above
        for place in gmaps_result:
            try: 
                placeId = place['place_id']
                details = gmaps.place(place_id=placeId, fields=my_fields)
                details = remove_types(details)
                jsonData[f"{bType}"].append(details['result'])
            except:
                continue
                

    print("return jsonData")
    return jsonData

# End of Places_API
    