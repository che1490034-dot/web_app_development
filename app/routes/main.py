from flask import render_template, request, redirect, url_for, flash, session
from app.routes import main_bp
from app.models.place import Place, Review
from app.models.itinerary import Itinerary

@main_bp.route('/')
def index():
    # 這裡可以抓取一些精選景點
    places = Place.query.limit(6).all()
    return render_template('index.html', places=places)

@main_bp.route('/places')
def list_places():
    places = Place.get_all()
    return render_template('places/index.html', places=places)

@main_bp.route('/places/<int:place_id>')
def place_detail(place_id):
    place = Place.get_by_id(place_id)
    if not place:
        return "找不到景點", 404
    return render_template('places/detail.html', place=place)

@main_bp.route('/places/<int:place_id>/reviews', methods=['POST'])
def add_review(place_id):
    if 'user_id' not in session:
        flash('請先登入才能發表評價！', 'warning')
        return redirect(url_for('auth.login'))
        
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if not rating:
        flash('請給予評分！', 'danger')
        return redirect(url_for('main.place_detail', place_id=place_id))
        
    Review.create(place_id=place_id, user_id=session['user_id'], rating=int(rating), comment=comment)
    flash('評價發表成功！', 'success')
    return redirect(url_for('main.place_detail', place_id=place_id))

@main_bp.route('/shared/<string:share_code>')
def view_shared_itinerary(share_code):
    itinerary = Itinerary.query.filter_by(share_code=share_code, is_shared=True).first()
    if not itinerary:
        return "找不到此分享行程或該行程已關閉分享", 404
    return render_template('itineraries/shared.html', itinerary=itinerary)
