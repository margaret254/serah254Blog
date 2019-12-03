from flask import render_template,redirect,url_for, abort,request,flash
from . import main
from ..requests import get_quotes

from .forms import CommentsForm ,UpdateProfile, BlogForm
from ..models import User,Blog, Comment
from flask_login import login_required, current_user
from .. import db, photos
import markdown2
from ..email import mail_message


   

# Views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome this is where you belong'

    
    blogs= Blog.get_all_blogs() 
    quotes = get_quotes() 

    return render_template('index.html', title = title, quotes = quotes, blogs= blogs)

@main.route('/about')
def about():
    '''
    View root page function that returns the about page and its data
    '''
    title = ''
    return render_template('about.html', title=title)

@main.route('/contact')
def contact():
    '''
    View root page function that returns the contact page and its data
    '''
    title = ''
    return render_template('contacts.html', title = title)

@main.route('/all')
def all():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome this is where you belong'

    
    blogs= Blog.get_all_blogs() 
    

    return render_template('index.html', title = title, blogs= blogs)



@main.route('/blog/<int:blog_id>')
def blog(blog_id):

    '''
    View blog page function that returns the blog details page and its data
    '''
    found_blog= Blog.query.get(blog_id)
    title = blog_id
    blog_comments = Comment.get_comments(blog_id)

    return render_template('blog.html',title= title ,found_blog= found_blog, blog_comments= blog_comments)


@main.route("/blog/<int:blog_id>/update", methods=['GET', 'POST'])
def update_post(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.blog', blog_id=blog.id))
    elif request.method == 'GET':
        blog.title.data = blog.title
        blog.content.data = blog.content
    return render_template('blog.html', title='Update Blog', form=form)

@main.route("/blog/<int:blog_id>/delete", methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.index'))



@main.route('/blog/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    '''
    Function that creates new blogs
    '''
    form = BlogForm()


    if form.validate_on_submit():
        blog = Blog(title=form.title.data,blog=form.content.data)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('new_blog.html', new_blog_form= form)

@main.route('/blog/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    if form.validate_on_submit():
        new_comment = Comment(blog_id =id,comment=form.comment.data,username=current_user.username)
        new_comment.save_comments()
        return redirect(url_for('main.all'))
    
    return render_template('new_comment.html',comment_form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path 
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)

@main.route('/view/comment/<int:id>')
def view_comments(id):
    '''
    Function that returns  the comments belonging to a particular blog
    '''
    comments = Comment.get_comments(id)
    return render_template('view_comment.html',comments = comments, id=id)



@main.route('/test/<int:id>')  
def test(id):
    '''
    this is route for basic testing
    '''
    blog =Blog.query.filter_by(id=1).first()
    return render_template('test.html',blog= blog)

#sSubscribe
@main.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    '''
    Function to send email upon subscription
    '''
    if request.method == 'POST':
        email = request.form['email']
        new_email = Subscribe(email=email)
        db.session.add(new_email)
        db.session.commit()
        flash('Thank you for your subscription')
        return redirect(url_for('index'))
        

