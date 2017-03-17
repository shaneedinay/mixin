# Mixin Default Controller
# Version 1.0.0
# March 17, 2017
# -*- coding: utf-8 -*-

# TORNADO SSD
from gluon.contrib.websocket_messaging import websocket_send
from datetime import datetime
from datetime import tzinfo

def index():
    if (auth.is_logged_in()):
        redirect(URL('home'))
    form = auth()
    if response.title:
        welcomemessage = "Welcome to %s" % response.title
    else:
        welcomemessage = "Welcome"
    return dict(message=T(welcomemessage), form=form)

def user():
    return dict(form=auth())

@auth.requires_login()
def home():
    author = auth.user.id
    authorfn = auth.user.first_name
    authorln = auth.user.last_name
    currentfollow = db().select(db.followers.ALL, orderby=db.followers.id)

    # Friends Lists
    followerlist = (DIV(""))
    for i in currentfollow:
       if i.user_id == author:
           following = i.following_id
           followerlist += (DIV(SPAN('', _class='glyphicon glyphicon-user mi-add-to-mr'), name_of(following)))
    #Form Search friendlist
    User = db.auth_user
    alphabetical = db.auth_user.first_name|db.auth_user.last_name
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        tokens = form.vars.name.split()
        query = reduce(lambda a,b:a&b,
                       [User.first_name.contains(k)|User.last_name.contains(k) \
                            for k in tokens])
        people = db(query).select(orderby=alphabetical)
    else:
        people = []
    # Chatroom form
    chatform = SQLFORM(db.chatRoom)
    if chatform.process(keepvalues=True).accepted:
       redirect(URL('home'))
    allChatRooms = db().select(db.chatRoom.ALL, orderby=db.chatRoom.id)
    chatRooms = allChatRooms.find(lambda row: author in row.members)
    # Add Member to Chatroom
    return dict(followerlist=followerlist, form=form, people=people, author=author, chatRooms=chatRooms, chatform=chatform, currentfollow=currentfollow)

@auth.requires_login()
def musicroom():


    currentmembers = db().select(db.chatRoom.ALL, orderby=db.chatRoom.name)
    isAuthorized = False
    for i in currentmembers:
        if i.id == long(request.args[0]):
            for j in i.members:
                if j == auth.user.id:
                    isAuthorized = True

    if not(isAuthorized):
        redirect(URL('home'))

    r_id = request.args[0]
    check = db(db.chatRoom.id == r_id).select().first()
    if not (check):
        redirect(URL('home'))

    users = db().select(db.auth_user.ALL, orderby=db.auth_user.id)
    friendlist = (LI(""))
    for i in users:
        if i.id in db.chatRoom(request.args[0]).members:
            friendlist += (LI("%s" % i.username))

    your_friends = db(auth.user.id == db.followers.user_id).select(db.followers.ALL, orderby=db.followers.id)        
    chatroomName = db(db.chatRoom.id == r_id).select(db.chatRoom.name)[0].name
    #show only last 10 messages so chat to prevent lag
    chats = db(db.chat.room_id == r_id).select(orderby=~db.chat.id,limitby=(0,10))
    chatRoomUp = db(db.chatRoom.id == r_id).select(db.chatRoom.up_votes)[0].up_votes
    chatRoomDown = db(db.chatRoom.id == r_id).select(db.chatRoom.down_votes)[0].down_votes
    return dict(message=T('%(first_name)s\'s music room' % auth.user), friendlist=friendlist,chats=chats,chatroomName=chatroomName,chatRoomUp=chatRoomUp,chatRoomDown=chatRoomDown,your_friends=your_friends)
    #return users

@auth.requires_login()
def settings():
    return dict(form=auth())

@auth.requires_login()
def about():
    return dict()

@auth.requires_login()
def contact():
    return dict()

# This is the Ajax callback to follow and unfollow users
@auth.requires_login()
def friendship():
    """AJAX callback!"""
    me, a0, a1 = auth.user_id, request.args(0), request.args(1)
    FT = db.followers
    if request.env.request_method!='POST': raise HTTP(400)
    if a0=='request' and not FT(user_id=a1, following_id=me):
        # insert a new follow
        if not db(FT.user_id==me)(FT.following_id==request.args(1)).count():
            FT.insert(user_id=me, following_id=a1)
    elif a0=='delete':
        # delete a  follow
        db(FT.user_id==me)(FT.following_id==a1).delete()

    # Update Friends Lists
    author = auth.user.id;
    currentfollow = db().select(db.followers.ALL, orderby=db.followers.id)
    followerlist = (DIV(""))
    for i in currentfollow:
       if i.user_id == author:
           following = i.following_id
           followerlist += (DIV(SPAN('', _class='glyphicon glyphicon-user mi-add-to-mr'), name_of(following)))
    return str(followerlist)

def new_message():
    form = SQLFORM(Chat)

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messageSent = "<b>" + auth.user.username + ":</b>" + request.vars.your_message + "</br>" + str(date)
    chatroomId = request.vars.room_id
    websocketURL = request.vars.wsURL
    # TORNADO SSD
    if form.accepts(request, formname=None):
         websocket_send('http://' + websocketURL +':8888', messageSent, 'mykey', 'chatroom' + chatroomId )
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])
    return ()

def voteup():
    post = db.chatRoom(request.vars.room_id)
    vote_list = post.vote_up_list
    if auth.user.id in vote_list:
        vote_list.remove(auth.user.id)
        post.update_record(vote_up_list=list(set(vote_list)))
        new_votes = post.up_votes - 1
        post.update_record(up_votes=new_votes)
        if new_votes < 0:
            new_votes = 0
        return str(new_votes)
    else:
        vote_list.append(auth.user.id)
        post.update_record(vote_up_list=list(set(vote_list)))
        new_votes = post.up_votes + 1
        post.update_record(up_votes=new_votes)
        return str(new_votes)


def votedown():
    post = db.chatRoom(request.vars.room_id)
    vote_list = post.vote_down_list
    if auth.user.id in vote_list:
        vote_list.remove(auth.user.id)
        post.update_record(vote_down_list=list(set(vote_list)))
        new_votes = post.down_votes - 1
        post.update_record(down_votes=new_votes)
        if new_votes < 0:
            new_votes = 0
        return str(new_votes)
    else:
        vote_list.append(auth.user.id)
        post.update_record(vote_down_list=list(set(vote_list)))
        new_votes = post.down_votes + 1
        post.update_record(down_votes=new_votes)
        return str(new_votes)

def addurlmes():
    # not working
    #db(Chat).author=auth.user.first_name
    CR = db.chat
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messageSent = "<b>" + auth.user.username + ":</b>" + request.vars.mi_url + "</br>" + str(date)
    print(request.vars.mi_url)
    chatroomId = request.vars.room_id
    websocketURL = request.vars.wsURL
    # TORNADO SSD
    websocket_send('http://' + websocketURL +':8888', messageSent, 'mykey', 'chatroom' + chatroomId )
    CR.insert(your_message=request.vars.mi_url, room_id=chatroomId)
    return ()

def join_room():
    friend_to_add_id = int(request.vars.addFriend)
    room_id = request.vars.room_id
    chat_room = db.chatRoom(room_id)
    members_list = chat_room.members
    friend_to_add = db.auth_user(friend_to_add_id)
    if friend_to_add_id in members_list:
        response.flash = "%s is already in this room" % name_of(friend_to_add)
        return ()
    else:
        members_list.append(friend_to_add)
        chat_room.update_record(members = list(set(members_list)))
        response.flash = "Added %s" % name_of(friend_to_add)
        return "$('#friendlisttt').append('<li>%s</li>');" % friend_to_add.username
@cache.action()
def download():
    return response.download(request, db)

def call():
    return service()
