# Mixin Default Controller
# Version 1.0.0
# March 17, 2017
# -*- coding: utf-8 -*-

# TORNADO SSD
from gluon.contrib.websocket_messaging import websocket_send

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
           followerlist += (DIV(BUTTON('', _id=following, _class='btn btn-sm btn-default glyphicon glyphicon-plus mi-add-to-mr'), name_of(following)))
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
    chatRooms = db().select(db.chatRoom.ALL, orderby=db.chatRoom.id)
    # Add Member to Chatroom
    return dict(followerlist=followerlist, form=form, people=people, author=author, chatRooms=chatRooms, chatform=chatform, currentfollow=currentfollow)

@auth.requires_login()
def musicroom():
    r_id = request.args[0]
    check = db(db.chatRoom.id == r_id).select().first()
    if not (check):
        redirect(URL('home'))

    users = db().select(db.auth_user.ALL, orderby=db.auth_user.id)
    friendlist = (LI(""))
    for i in users:
        friendlist += (LI("%s" % i.first_name))
    chatroomName = db(db.chatRoom.id == r_id).select(db.chatRoom.name)[0].name
    chats = db(db.chat.room_id == r_id).select(orderby=db.chat.time_created)
    chatRoomUp = db(db.chatRoom.id == r_id).select(db.chatRoom.up_votes)[0].up_votes
    chatRoomDown = db(db.chatRoom.id == r_id).select(db.chatRoom.down_votes)[0].down_votes
    return dict(message=T('%(first_name)s\'s music room' % auth.user), friendlist=friendlist,chats=chats,chatroomName=chatroomName,chatRoomUp=chatRoomUp,chatRoomDown=chatRoomDown)
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
           followerlist += (DIV(BUTTON('', _id=following, _class='btn btn-sm btn-default glyphicon glyphicon-plus mi-add-to-mr'), name_of(following)))
    return str(followerlist)

def new_message():
    form = SQLFORM(Chat)
    # not working
    #db(Chat).author=auth.user.first_name
    messageSent = request.vars.your_message
    chatroomId = request.vars.room_id
    websocketURL = request.vars.wsURL
    print (websocketURL)
    # TORNADO SSD
    default  websocket_send('http://127.0.0.1:8888', messageSent, 'mykey', 'mygroup')
    if form.accepts(request, formname=None):
         websocket_send('http://' + websocketURL +':8888', messageSent, 'mykey', 'chatroom' + chatroomId )
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])
    return ()

def voteup():
    post = db.chatRoom[(request.vars.room_id)]
    new_votes = post.up_votes + 1
    post.update_record(up_votes=new_votes)
    return str(new_votes)

def votedown():
    post = db.chatRoom[(request.vars.room_id)]
    new_votes = post.down_votes + 1
    post.update_record(down_votes=new_votes)
    return str(new_votes)

def addurlmes():
    # not working
    #db(Chat).author=auth.user.first_name
    CR = db.chat
    messageSent = request.vars.mi_url
    print(request.vars.mi_url)
    chatroomId = request.vars.room_id
    # TORNADO SSD
    websocket_send('http://127.0.0.1:8888', messageSent, 'mykey', 'chatroom' + chatroomId )
    CR.insert(your_message=messageSent, room_id=chatroomId)
    return ()

@cache.action()
def download():
    return response.download(request, db)

def call():
    return service()
