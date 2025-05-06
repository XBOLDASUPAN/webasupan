from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
import uuid
from functools import wraps

# Konfigurasi logging
logging.basicConfig(
    filename='log.txt',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YR8k9#mP2$vL5nQ7@jX4hC1wB6tF3sD0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['DEV_MODE'] = os.environ.get('FLASK_ENV') == 'development'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
VIDEOS_PER_PAGE = 9  # Jumlah video per halaman

# Tambahkan error handler
@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f'Unhandled error: {str(error)}', exc_info=True)
    return 'Internal Server Error', 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Page not found: {request.url}')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return render_template('errors/500.html'), 500

@app.errorhandler(401)
def unauthorized_error(error):
    app.logger.error(f'Unauthorized access: {request.url}')
    return redirect(url_for('admin_login'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

# Association table for Video-Tag many-to-many relationship
video_tags = db.Table('video_tags',
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# Konfigurasi Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Silakan login terlebih dahulu.'
login_manager.login_message_category = 'warning'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    videos = db.relationship('Video', backref='category', lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    videos = db.relationship('Video', secondary=video_tags, backref=db.backref('tags', lazy='dynamic'))

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        app.logger.error(f'Error loading user: {str(e)}')
        return None

def is_dev_mode():
    return app.config['DEV_MODE']

@app.context_processor
def inject_dev_mode():
    return dict(dev_mode=is_dev_mode())

@app.route('/')
def index():
    try:
        page = request.args.get('page', 1, type=int)
        search_query = request.args.get('q', '')
        category_id = request.args.get('category')
        
        if search_query:
            videos = Video.query.filter(Video.title.ilike(f'%{search_query}%'))
        elif category_id:
            videos = Video.query.filter_by(category_id=category_id)
        else:
            videos = Video.query
            
        videos = videos.order_by(Video.created_at.desc())
        videos = videos.paginate(page=page, per_page=VIDEOS_PER_PAGE, error_out=False)
        categories = Category.query.all()
        
        return render_template('index.html', videos=videos, categories=categories, search_query=search_query)
    except Exception as e:
        app.logger.error(f'Error in index route: {str(e)}')
        raise

@app.route('/category/<int:id>')
def category(id):
    try:
        page = request.args.get('page', 1, type=int)
        category = Category.query.get_or_404(id)
        videos = Video.query.filter_by(category_id=id).order_by(Video.created_at.desc()).paginate(page=page, per_page=VIDEOS_PER_PAGE, error_out=False)
        categories = Category.query.all()
        return render_template('category.html', category=category, videos=videos, categories=categories)
    except Exception as e:
        app.logger.error(f'Error in category route: {str(e)}')
        raise

@app.route('/tag/<int:id>')
def tag(id):
    try:
        tag = Tag.query.get_or_404(id)
        page = request.args.get('page', 1, type=int)
        
        # Gunakan join untuk mendapatkan video yang terkait dengan tag
        videos = Video.query.join(Video.tags).filter(Tag.id == id)\
            .order_by(Video.created_at.desc())\
            .paginate(page=page, per_page=VIDEOS_PER_PAGE, error_out=False)
            
        categories = Category.query.all()
        return render_template('tag.html', 
                            videos=videos, 
                            tag=tag,
                            categories=categories)
    except Exception as e:
        app.logger.error(f'Error in tag route: {str(e)}')
        raise

@app.route('/latest')
def latest():
    try:
        page = request.args.get('page', 1, type=int)
        videos = Video.query.order_by(Video.created_at.desc()).paginate(page=page, per_page=VIDEOS_PER_PAGE, error_out=False)
        categories = Category.query.all()
        return render_template('latest.html', videos=videos, categories=categories)
    except Exception as e:
        app.logger.error(f'Error in latest route: {str(e)}')
        raise

@app.route('/popular')
def popular():
    try:
        page = request.args.get('page', 1, type=int)
        videos = Video.query.order_by(Video.views.desc()).paginate(page=page, per_page=VIDEOS_PER_PAGE, error_out=False)
        categories = Category.query.all()
        return render_template('popular.html', videos=videos, categories=categories)
    except Exception as e:
        app.logger.error(f'Error in popular route: {str(e)}')
        raise

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    try:
        app.logger.info('Accessing admin page')
        page = request.args.get('page', 1, type=int)
        app.logger.debug(f'Page number: {page}')
        
        videos = Video.query.order_by(Video.created_at.desc())
        app.logger.debug('Got videos query')
        
        paginated_videos = videos.paginate(page=page, per_page=VIDEOS_PER_PAGE, error_out=False)
        app.logger.debug(f'Paginated videos: {paginated_videos.total} total items')
        
        categories = Category.query.all()
        app.logger.debug(f'Got {len(categories)} categories')
        
        tags = Tag.query.all()
        app.logger.debug(f'Got {len(tags)} tags')
        
        return render_template('admin.html', videos=paginated_videos, categories=categories, tags=tags)
    except Exception as e:
        app.logger.error(f'Error in admin route: {str(e)}', exc_info=True)
        raise

@app.route('/view/<int:id>')
def view_video(id):
    try:
        video = Video.query.get_or_404(id)
        video.views += 1
        db.session.commit()
        return redirect(video.video_url)
    except Exception as e:
        app.logger.error(f'Error viewing video: {str(e)}')
        return redirect(url_for('index'))

@app.route('/add_video', methods=['POST'])
@login_required
def add_video():
    try:
        title = request.form.get('title')
        video_url = request.form.get('video_url')
        category_id = request.form.get('category_id')
        tag_ids = request.form.getlist('tags')  # Mengambil multiple tag IDs
        thumbnail_type = request.form.get('thumbnail_type')
        
        video = Video(title=title, video_url=video_url)
        
        # Set category jika ada
        if category_id:
            video.category_id = category_id
            
        # Set thumbnail
        if thumbnail_type == 'url':
            video.thumbnail_url = request.form.get('thumbnail_url')
        elif thumbnail_type == 'file':
            if 'thumbnail_file' not in request.files:
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(url_for('admin'))
                
            file = request.files['thumbnail_file']
            if file.filename == '':
                flash('Tidak ada file yang dipilih', 'danger')
                return redirect(url_for('admin'))
                
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                video.thumbnail_url = url_for('static', filename=f'uploads/{filename}')
        
        # Tambahkan tag yang dipilih
        if tag_ids:
            selected_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            video.tags.extend(selected_tags)
        
        db.session.add(video)
        db.session.commit()
        
        flash('Video berhasil ditambahkan', 'success')
        return redirect(url_for('admin'))
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error in add_video: {str(e)}')
        flash('Terjadi kesalahan saat menambahkan video', 'danger')
        return redirect(url_for('admin'))

@app.route('/add_tag', methods=['POST'])
@login_required
def add_tag():
    try:
        name = request.form.get('name')
        if name:
            existing_tag = Tag.query.filter_by(name=name).first()
            if existing_tag:
                flash('Tag dengan nama tersebut sudah ada!', 'error')
            else:
                tag = Tag(name=name)
                db.session.add(tag)
                db.session.commit()
                flash('Tag berhasil ditambahkan!', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f'Error adding tag: {str(e)}')
        db.session.rollback()
        flash('Terjadi kesalahan saat menambahkan tag!', 'error')
        return redirect(url_for('admin'))

@app.route('/edit_tag/<int:id>', methods=['POST'])
@login_required
def edit_tag(id):
    try:
        tag = Tag.query.get_or_404(id)
        new_name = request.form.get('name')
        if new_name:
            existing_tag = Tag.query.filter_by(name=new_name).first()
            if existing_tag and existing_tag.id != id:
                flash('Tag dengan nama tersebut sudah ada!', 'error')
            else:
                tag.name = new_name
                db.session.commit()
                flash('Tag berhasil diperbarui!', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f'Error editing tag: {str(e)}')
        db.session.rollback()
        flash('Terjadi kesalahan saat memperbarui tag!', 'error')
        return redirect(url_for('admin'))

@app.route('/admin/delete_tag/<int:id>', methods=['POST'])
@login_required
def delete_tag(id):
    try:
        tag = Tag.query.get_or_404(id)
        db.session.delete(tag)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting tag: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/add_category', methods=['POST'])
@login_required
def add_category():
    try:
        name = request.form.get('name')
        if name:
            existing_category = Category.query.filter_by(name=name).first()
            if existing_category:
                flash('Kategori dengan nama tersebut sudah ada!', 'error')
            else:
                category = Category(name=name)
                db.session.add(category)
                db.session.commit()
                flash('Kategori berhasil ditambahkan!', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f'Error adding category: {str(e)}')
        db.session.rollback()
        flash('Terjadi kesalahan saat menambahkan kategori!', 'error')
        return redirect(url_for('admin'))

@app.route('/edit_category/<int:id>', methods=['POST'])
@login_required
def edit_category(id):
    try:
        category = Category.query.get_or_404(id)
        new_name = request.form.get('name')
        if new_name:
            existing_category = Category.query.filter_by(name=new_name).first()
            if existing_category and existing_category.id != id:
                flash('Kategori dengan nama tersebut sudah ada!', 'error')
            else:
                category.name = new_name
                db.session.commit()
                flash('Kategori berhasil diperbarui!', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f'Error editing category: {str(e)}')
        db.session.rollback()
        flash('Terjadi kesalahan saat memperbarui kategori!', 'error')
        return redirect(url_for('admin'))

@app.route('/delete_category/<int:id>')
@login_required
def delete_category(id):
    try:
        category = Category.query.get_or_404(id)
        # Update video yang menggunakan kategori ini
        Video.query.filter_by(category_id=id).update({Video.category_id: None})
        db.session.delete(category)
        db.session.commit()
        flash('Kategori berhasil dihapus!', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f'Error deleting category: {str(e)}')
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus kategori!', 'error')
        return redirect(url_for('admin'))

@app.route('/delete_video/<int:id>')
@login_required
def delete_video(id):
    try:
        video = Video.query.get_or_404(id)
        db.session.delete(video)
        db.session.commit()
        flash('Video berhasil dihapus!', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f'Error deleting video: {str(e)}')
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus video!', 'error')
        return redirect(url_for('admin'))

@app.route('/admin/delete_all_videos', methods=['POST'])
@login_required
def delete_all_videos():
    try:
        Video.query.delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting all videos: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/delete_all_categories', methods=['POST'])
@login_required
def delete_all_categories():
    try:
        # Hapus semua video terlebih dahulu karena ada foreign key
        Video.query.delete()
        Category.query.delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting all categories: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/delete_all_tags', methods=['POST'])
@login_required
def delete_all_tags():
    try:
        # Hapus semua relasi video-tag
        db.session.execute(video_tags.delete())
        Tag.query.delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting all tags: {str(e)}')
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/toggle_dev_mode', methods=['POST'])
@login_required
def toggle_dev_mode():
    try:
        app.config['DEV_MODE'] = not app.config['DEV_MODE']
        status = 'aktif' if app.config['DEV_MODE'] else 'nonaktif'
        flash(f'Development Mode {status}', 'success')
        return redirect(url_for('admin'))
    except Exception as e:
        app.logger.error(f'Error toggling dev mode: {str(e)}')
        flash('Terjadi kesalahan saat mengubah mode!', 'error')
        return redirect(url_for('admin'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('admin'))
            
            flash('Username atau password salah!', 'error')
        return render_template('login.html')
    except Exception as e:
        app.logger.error(f'Error in login route: {str(e)}')
        raise

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f'Error in logout route: {str(e)}')
        raise

if __name__ == '__main__':
    with app.app_context():
        # Create instance directory if it doesn't exist
        instance_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)
            
        # Create all database tables
        db.create_all()
        
        # Create default admin user if not exists
        admin = User.query.filter_by(username='YADIRC').first()
        if not admin:
            admin = User(username='YADIRC')
            admin.password_hash = generate_password_hash('YadiRc120502')
            db.session.add(admin)
            db.session.commit()
            
        app.run(debug=True)
