import random
from .local import *
import requests

resp_js = None

is_private = False
total_uploads = 12
cookie = {"sessionid": "your session id"}


def get_page(username):
    global resp_js
    session = requests.session()
    session.headers = {'User-Agent': random.choice(useragent)}
    resp_js = session.get(f'https://www.instagram.com/{username}/?__a=1', cookies=cookie).json()
    return resp_js


banner_i()


def user_info(username):
    global total_uploads, is_private

    js = get_page(username)
    js = js['graphql']['user']

    if js['is_private'] != False:
        is_private = True

    if js['edge_owner_to_timeline_media']['count'] > 12:
        pass
    else:
        total_uploads = js['edge_owner_to_timeline_media']['count']

    userinfo = {
        'username': js['username'],
        'user id': js['id'],
        'name': js['full_name'],
        'followers': js['edge_followed_by']['count'],
        'following': js['edge_follow']['count'],
        'posts img': js['edge_owner_to_timeline_media']['count'],
        'posts vid': js['edge_felix_video_timeline']['count'],
        'reels': js['highlight_reel_count'],
        'bio': js['biography'].replace('\n', ', '),
        'external url': js['external_url'],
        'private': js['is_private'],
        'verified': js['is_verified'],
        'profile img': urlshortner(js['profile_pic_url_hd']),
        'business account': js['is_business_account'],
        # 'connected to fb': js['connected_fb_page'],  -- requires login
        'joined recently': js['is_joined_recently'],
        'business category': js['business_category_name'],
        'category': js['category_enum'],
        'has guides': js['has_guides'],
    }

    print(f"{su}{re} user info")
    for key, val in userinfo.items():
        print(f"  {gr}%s : {wh}%s" % (key, val))

    print("")
    return username


def highlight_post_info(all_data, photo_number):
    postinfo = {}
    total_child = 0
    child_img_list = []
    user = all_data['graphql']['user']
    node = user['edge_owner_to_timeline_media']['edges'][photo_number]['node']

    # this info will be same on evry post
    info = {
        'comments': node['edge_media_to_comment']['count'],
        'comment disable': node['comments_disabled'],
        'timestamp': node['taken_at_timestamp'],
        'likes': node['edge_liked_by']['count'],
        'location': node['location'],
    }

    # if image dosen't have caption this key dosen't exist instead of null
    try:
        info['caption'] = all_data['graphql']['user']['edge_media_to_caption']['edges'][0]['node']['text']
    except KeyError:
        pass

    # if uploder has multiple images / vid in single post get info how much edges are
    if 'edge_sidecar_to_children' in node:
        total_child = len(node['edge_sidecar_to_children']['edges'])

        for child in range(total_child):
            data = all_data['graphql']['user']['edge_owner_to_timeline_media']['edges'][photo_number]['node']['edge_sidecar_to_children'][
                'edges'][child]['node']
            img_info = {
                'typename': data['__typename'],
                'id': data['id'],
                'shortcode': data['shortcode'],
                'dimensions': str(data['dimensions']['height'] + data['dimensions']['width']),
                'image url': data['display_url'],
                'fact check overall': data['fact_check_overall_rating'],
                'fact check': data['fact_check_information'],
                'gating info': data['gating_info'],
                'media overlay info': data['media_overlay_info'],
                'is_video': data['is_video'],
                'accessibility': data['accessibility_caption']
            }

            child_img_list.append(img_info)

        postinfo['imgs'] = child_img_list
        postinfo['info'] = info

    else:
        info = {
            'comments': node['edge_media_to_comment']['count'],
            'comment disable': node['comments_disabled'],
            'timestamp': node['taken_at_timestamp'],
            'likes': node['edge_liked_by']['count'],
            'location': node['location'],
        }

        try:
            info['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            pass

        img_info = {
            'typename': node['__typename'],
            'id': node['id'],
            'shortcode': node['shortcode'],
            'dimensions': str(node['dimensions']['height'] + node['dimensions']['width']),
            'image url': node['display_url'],
            'fact check overall': node['fact_check_overall_rating'],
            'fact check': node['fact_check_information'],
            'gating info': node['gating_info'],
            'media overlay info': node['media_overlay_info'],
            'is_video': node['is_video'],
            'accessibility': node['accessibility_caption']
        }

        child_img_list.append(img_info)

        postinfo['imgs'] = child_img_list
        postinfo['info'] = info

    return postinfo


def post_info(username):
    if is_private != False:
        print(f"{fa} {gr}cannot use -p for private accounts !\n")
        sys.exit(1)

    posts = []
    data = get_page(username)  # Сюда
    for x in range(total_uploads):
        posts.append(highlight_post_info(data, x))

    for x in range(len(posts)):
        # get 1 item from post list
        print(f"{su}{re} post %s :" % x)
        for key, val in posts[x].items():
            if key == 'imgs':
                # how many child imgs post has
                postlen = len(val)
                # loop over all child img
                print(f"{su}{re} contains %s media" % postlen)
                for y in range(postlen):
                    # print k,v of all child img in loop
                    for xkey, xval in val[y].items():
                        print(f"  {gr}%s : {wh}%s" % (xkey, xval))
            if key == 'info':
                print(f"{su}{re} info :")
                for key, val in val.items():
                    print(f"  {gr}%s : {wh}%s" % (key, val))
                print("")
