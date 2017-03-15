# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
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
        # response.flash str(query)
        people = db(query).select(orderby=alphabetical)
        # db(people.id == author).delete()
        # for user in people:
            # if db(user.first_name==authorfn, user.last_name==authorln).count():
                # db(people.user==author).delete()
        # if db(people.first_name==auth)(VU.uid==me).count():
    else:
        people = []
    # return dict(friendlist=friendlist, requestlist=requestlist, form=form, people=people, friendtable=users, author=author)
    chatform = SQLFORM(db.chatRoom)
    if chatform.process(keepvalues=True).accepted:
       redirect(URL('home'))
    chatRooms = db().select(db.chatRoom.ALL, orderby=db.chatRoom.id)
    return dict(followerlist=followerlist, form=form, people=people, author=author, chatRooms=chatRooms, chatform=chatform, currentfollow=currentfollow)

@auth.requires_login()
def musicroom():
    """author = auth.user.id;
    users = db().select(db.friend_table.ALL, orderby=db.friend_table.id)
    friendlist = (DIV(""))
    for i in users:
        if i.accepted:
            if i.user_id == author:
                friend = i.friend_user_id
                friendlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
            elif i.friend_user_id == author:
                friend = i.user_id
                friendlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
    return dict(friendlist=friendlist)"""
    number = db.chatRoom[request.args(0)]
    if not(number):
        redirect(URL('home'))
    roomname = number.name
    return dict(number=number, roomname=roomname)

@auth.requires_login()
def settings():
    return dict(form=auth())

@auth.requires_login()
def about():
    return dict()

@auth.requires_login()
def contact():
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

@auth.requires_login()
def mbrain():
    return dict()

@auth.requires_login()
def sdinay():
    # author = auth.user.id;
    # users = db().select(db.friend_table.ALL, orderby=db.friend_table.id)
    # friendlist = (DIV(""))
    # for i in users:
        # if i.accepted:
            # if i.user_id == author:
                # friend = i.friend_user_id
                # friendlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
            # elif i.friend_user_id == author:
                # friend = i.user_id
                # friendlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
    # return dict(friendlist=friendlist)
    number = db.chatRoom[request.args(0)]
    roomname = number.name
    return dict(number=number, roomname=roomname)

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
