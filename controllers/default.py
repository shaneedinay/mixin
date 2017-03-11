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
    # Chapter 09 Authorization
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@auth.requires_login()
def home():
    author = auth.user.id;
    users = db().select(db.friend_table.ALL, orderby=db.friend_table.id)
    # Friends Lists
    friendlist = (DIV(""))
    for i in users:
        if i.accepted:
            if i.user_id == author:
                friend = i.friend_user_id
                friendlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
            elif i.friend_user_id == author:
                friend = i.user_id
                friendlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
    # Requests Lists
    requestlist = (DIV(""))
    for i in users:
        if not i.accepted:
            if i.user_id == author:
                friend = i.friend_user_id
                requestlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
            elif i.friend_user_id == author:
                friend = i.user_id
                requestlist += (DIV("%s %s" % (friend.first_name, friend.last_name)))
    #Form Search friendlist
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        tokens = form.vars.name.split()
        query = reduce(lambda a,b:a&b,
                       [db.auth_user.first_name.contains(k)|db.auth_user.last_name.contains(k) \
                            for k in tokens])
        people = db(query).select(orderby=db.auth_user.first_name|db.auth_user.last_name)
    else:
        people = []
    return dict(friendlist=friendlist, requestlist=requestlist, form=form, people=people, friendtable=users, author=author)

@auth.requires_login()
def musicroom():
    author = auth.user.id;
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
    return dict(friendlist=friendlist)

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
    FT = db.friend_table
    if request.env.request_method!='POST': raise HTTP(400)
    if a0=='request' and not FT(user_id=a1,friend_user_id=me):
        # insert a new friendship request
        FT.insert(user_id=me,friend_user_id=a1)
    #elif a0=='accept':
        # accept an existing friendship request
    #    db(FT.friend_user_id==me)(FT.user_id==request.args(0)).update(accepted=True)
    #    if not db(FT.user_id==me)(FT.friend_user_id==request.args(1)).count():
    #        FT.insert(user_id=me,friend_user_id=a1)
    #elif a0=='deny':
        # deny an existing friendship request
    #    db(FT.friend_user_id==me)(FT.user_id==a1).delete()
    #elif a0=='remove':
        # delete a previous friendship request
    #    db(FT.user_id==me)(FT.friend_user_id==a1).delete()

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
