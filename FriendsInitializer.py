from vk.exceptions import VkAPIError
from Database import Database
from ConfigAPI import ConfigAPI

class Initializer(object):
    def vk_refs(self, user_id, reference, api):
        if ('https://vk.com/' in reference):
            #         k = ConfigAPI()
            #         k.init()
            if ('id' in reference):
                us_split = reference.split('id')
                vk_us_id = us_split[1]
                #             проверка на ограничения юзера
                if (self.__check_account(vk_us_id, api)):
                    friends = api.friends.get(user_id=vk_us_id, extended=1)['items']
                    print('good')
                    if (2767201 in friends):
                        print('Бот в друзьях')
                    else:
                        print('добавьте бота в друзья')
                    #             add friends to db
                    db = Database()
                    db.check_vk_user(user_id, vk_us_id, friends)
                    print('added to db')
                else:
                    print('no fr')


            else:
                us_split = reference.split('/')
                us_nick = us_split[3]
                #             проверка на ограничения юзера, чекнуть можно ли вытащить айди у забаненного, ограниченного, чс юзера
                if (self.__check_account(us_nick, api)):
                    user = api.users.get(user_ids=[us_nick])
                    vk_us_id = user[0]['id']
                    friends = api.friends.get(user_id=vk_us_id, extended=1)['items']
                    print('good')
                    if (2767201 in friends):
                        print('true')
                    else:
                        print('добавьте бота в друзья')
                    #             add friends to db
                    db = Database()
                    db.check_vk_user(user_id, vk_us_id, friends)
                    print('added to db')
                else:
                    print('no fr')
        #             add friends to db
        else:
            print('Некорректная ссылка!')

    def __check_account(self, us_id, api):
        try:
            user = api.users.get(user_ids=us_id,
                                 fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')

            print('Обрабатывается: {} {}'.format(user[0]['first_name'], user[0]['last_name']))
            if (user[0].get('deactivated') != None):
                print('deactivated account: {}'.format(user[0]['id']))
                return False
            elif (user[0]['is_closed'] == 'True'):
                print('private account: {}'.format(user[0]['id']))
                return False
            elif (user[0].get('blacklisted') != None):
                if (user[0]['blacklisted'] == 1):
                    print('You are in the blacklist: {}'.format(user[0]['id']))
                    return False
                else:
                    return True
            else:
                return True
        except VkAPIError as e:
            if e.code == 18:
                print('account #{} is closed or deactivated!'.format(user[0]['id']))
                #                 self.init(api)
                return False

config = ConfigAPI()
config.init()
init = Initializer()
init.vk_refs(0, 'https://vk.com/id410235814', config.api)