# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    logger.info("Here we are, in the controller.")
    db.people.name.label = "What's your name?"
    logger.info("Session: %r" % session)
    row = db(db.people.user_id == auth.user_id).select().first()
    db.people.user_id.readable = db.people.user_id.writable = False
    form = SQLFORM(db.people, record=row)
    # board_list = [
    #     {'title': 'board1',},d
    #     {'title': 'board2',}
    # ]
    # return dict(board_list = board_list)
    redirect(URL('show_boards'))
    return dict(board_list = [])


@auth.requires_login()
def add_board():
    logger.info("My session is: %r" % session)
    form = SQLFORM(db.board)
    if form.process().accepted:
        session.flash = T('the data was inserted')
        redirect(URL('show_boards')) #might change to index
    return dict(form=form)

def show_boards():
    board_list = db(db.board).select()
    return dict(board_list=board_list)

#delete boards
def delete_post():
    post_id = request.args(0)
    db(db.posts.id == post_id).delete()
    redirect(URL('default','show_posts', args=request.args(1)))

def deleteboards():
    db(db.board.id > 0).delete()

def deleteposts():
    db(db.posts.id > 0).delete()


def show_posts():
    post_board_id = request.args(0)
    print "fuck"
    print post_board_id
    print "fuck again"
    post_list = db(db.posts.board==post_board_id).select()
    return dict(post_list=post_list, post_board_id=post_board_id)




def add_posts():


    logger.info("My session is: %r" % session)
    form = SQLFORM(db.posts)
    form.vars.board = request.args(0)
    form.vars.user_id = auth.user_id

    if form.process().accepted:
        session.flash = T('the data was inserted')
        redirect(URL('default','show_posts', args=request.args(0))) #might change to index
    return dict(form=form)

def posts_details():
    posts = db.posts(request.args)
    if posts is None:
        session.flash = T('No such post')
        redirect(URL('default', 'show_posts'))
    form = SQLFORM(db.posts, record=posts, readonly=True)
    edit_button = A('Edit', _class='btn btn-warning',
                    _href=URL('default', 'posts_edit', args=[posts.id]))
    list_button = A('View all', _class='btn btn-info',
                    _href=URL('default', 'show_posts'))
    return dict(form=form, edit_button=edit_button,
                list_button=list_button)
def posts_edit():
    posts = db.posts(request.args(0))
    if posts is None:
        session.flash = T('No such posts')
        redirect(URL('default', 'show_posts'))
    form = SQLFORM(db.posts, record=posts)
    if form.process().accepted:
        session.flash = T('The data was edited')
        redirect(URL('default', 'show_posts', args=[posts.board]))
    edit_button = A('View', _class='btn btn-warning',
                    _href=URL('default', 'show_posts', args=[posts.id]))
    return dict(form=form, edit_button=edit_button)



def posts():
    # board_id = request.args(0)
    # try:
    #     bid = int(board_id)
    # except Exception, e:
    #     session.message = T('Bad URL')
    #     redirect(URL('default', 'index'))
    # b = board_id.get(bid)
    # if b is None:
    #     session.message = T('no such board')
    #     redirect(URL('default', 'index'))
    # session.pasta_sauce = "Pesto" #not used
    return dict(post_list = [])




def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


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


