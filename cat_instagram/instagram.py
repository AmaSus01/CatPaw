import argparse
import lib.api as api
import geopy
import plotly.graph_objects as go

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--user", help="username of account to scan")
ap.add_argument("-p", "--post", action="store_true", help="image info of user uploads")
args = vars(ap.parse_args())

if args['user']:
    api.user_info(username=args["user"])

if args['post']:
    api.post_info(username=args["user"])


# def get_geolocation():
#     geoTag = input()
#     locator = geopy.Nominatim(user_agent='myGeocoder')
#     location = locator.geocode(geoTag)
#
#     #print("Latitude={}, Longitude={}".format(location.latitude, location.longitude))
#     map_access_token = open(".mapbox_token").read()
#
#     fig = go.Figure(go.Scattermapbox(
#         lat=[location.latitude],
#         lon=[location.longitude],
#         mode='markers',
#         marker=go.scattermapbox.Marker(size=14),
#         text=['Target'],
#     ))
#
#     fig.update_layout(
#         hovermode='closest',
#         mapbox=dict(
#             accesstoken=map_access_token,
#             bearing=0,
#             center=go.layout.mapbox.Center(
#                 lat=int(location.latitude),
#                 lon=int(location.longitude)
#             ),
#             pitch=0,
#             zoom=5
#         )
#     )
#     fig.show()
