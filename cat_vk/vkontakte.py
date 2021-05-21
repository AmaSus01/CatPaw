import argparse
from lib_vk.api_vk import getuser, get_friends, compare_search, print_user, banner

ap = argparse.ArgumentParser()
ap.add_argument("-uid", "--user_id", help="username id of account to scan")
ap.add_argument("-u", "--university", help="info about universities")
ap.add_argument("-c", "--city", help="info about city")
args = vars(ap.parse_args())

banner()

user_id = args.get('user_id')
university = args.get('university')
city = args.get('city')

search_fields = {
    'city': {city},
    'universities': {university}
    }

if user_id is not None:

    getuser(user_id=args["user_id"], fields=['city'])

    new_university = args.get('university')
    new_city = args.get('city')
    search_fields = dict()
    if new_university:
        search_fields['universities'] = new_university
    if new_city:
        search_fields['city'] = new_city
    friends_info = get_friends(user_id, list(search_fields.keys()))
    users = compare_search(friends_info, search_fields)
    # print(users)
    # all_users = set()
    # for user_id in users:
    #     friends_info = get_friends(user_id[1], list(search_fields.keys()))
    #     users = compare_search(friends_info, search_fields)
    #     print(users)
    #     all_users.update(users)
    # print(all_users)

fields = ['country', 'status', 'education', 'universities', 'bdate', 'last_seen', 'site', 'sex', 'screen_name',
          'schools', 'relation', 'relatives', 'photo_max_orig', 'exports', 'personal', 'occupation', 'music', 'movies',
          'activities', 'about', 'books', 'career', 'contacts', 'connections', 'city']
print_user(getuser(user_id, fields))