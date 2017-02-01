# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    form = auth()
    if response.title:
        welcomemessage = "Welcome to %s" % response.title
    else:
        welcomemessage = "Welcome"
    if form.process().accepted:
        redirect(URL('home'))
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

# @auth.requires_login()
def home():
    return dict(message=T('Hello %(first_name)s' % auth.user))
    #return dict(message=T("Hello %s", % auth.user))
    #return dict(message=('Hello'))

# @auth.requires_login()
def musicroom():
    return dict(message=T('This is the music room'), message2=T('Thanks for coming to %(first_name)s\'s music room' % auth.user))

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
