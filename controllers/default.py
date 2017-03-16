# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

from gluon.contrib.websocket_messaging import websocket_send

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if (auth.is_logged_in()):
        redirect(URL('home'))
    form = auth()
    if response.title:
        welcomemessage = "Welcome to %s" % response.title
    else:
        welcomemessage = "Welcome"
    #if form.process().accepted:
    #    redirect(URL('home'))
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

    chatform = SQLFORM(db.chatRoom)
    if chatform.process(keepvalues=True).accepted:
       redirect(URL('home'))
    chatRooms = db().select(db.chatRoom.ALL, orderby=db.chatRoom.id)
    return dict(followerlist=followerlist, form=form, people=people, author=author, chatRooms=chatRooms, chatform=chatform, currentfollow=currentfollow)

@auth.requires_login()
def musicroom():

    r_id = request.args[0]
    check = db(db.chatRoom.id == r_id).select().first()
    if not (check):
        redirect(URL('home'))

    users = db().select(db.auth_user.ALL, orderby=db.auth_user.id)
    #friendlist = (LI("%(first_name)s" % auth.user))
    friendlist = (LI(""))
    #friendlist = (LI("%s" % users[0].first_name))
    #friendlist = (LI("Start:"))
    #images[0].title
    #i = 0
    for i in users:
        #friendlist.append(LI("%s" % i.first_name))
        friendlist += (LI("%s" % i.first_name))
    #i = i + 1
    chatroomName = db(db.chatRoom.id == r_id).select(db.chatRoom.name)[0].name
    chats = db(db.chat.room_id == r_id).select(orderby=db.chat.time_created)

    return dict(message=T('%(first_name)s\'s music room' % auth.user), friendlist=friendlist,chats=chats,chatroomName=chatroomName)
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

@auth.requires_login()
def mbrain():
    return dict()

@auth.requires_login()
def sdinay():
    return dict()

@auth.requires_login()
def ryanho():
    return dict()

@auth.requires_login()
def jli306():
    return dict()

@auth.requires_login()
def katakeda():
    return dict()

@auth.requires_login()
def cdwheele():
    return dict()

# this is the Ajax callback
@auth.requires_login()
def friendship():
    """AJAX callback!"""
    me, a0, a1 = auth.user_id, request.args(0), request.args(1)
    FT = db.followers
    if request.env.request_method!='POST': raise HTTP(400)
    if a0=='request' and not FT(user_id=a1, following_id=me):
        # insert a new friendship request
        if not db(FT.user_id==me)(FT.following_id==request.args(1)).count():
            FT.insert(user_id=me, following_id=a1)
    #elif a0=='accept':
        # accept an existing friendship request
    #    db(FT.friend_user_id==me)(FT.user_id==request.args(0)).update(accepted=True)
    #    if not db(FT.user_id==me)(FT.friend_user_id==request.args(1)).count():
    #        FT.insert(user_id=me,friend_user_id=a1)
    #elif a0=='deny':
        # deny an existing friendship request
    #    db(FT.friend_user_id==me)(FT.user_id==a1).delete()
    elif a0=='delete':
        # delete a previous friendship request
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
    # default  websocket_send('http://127.0.0.1:8888', messageSent, 'mykey', 'mygroup')
    if form.accepts(request, formname=None):
         websocket_send('http://127.0.0.1:8888', messageSent, 'mykey', 'chatroom' + chatroomId )
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])
    return ()

def addurlmes():
    # not working
    #db(Chat).author=auth.user.first_name
    CR = db.chat
    messageSent = request.vars.mi_url
    print(request.vars.mi_url)
    chatroomId = request.vars.room_id
    websocket_send('http://127.0.0.1:8888', messageSent, 'mykey', 'chatroom' + chatroomId )
    CR.insert(your_message=messageSent, room_id=chatroomId)
    return ()


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
