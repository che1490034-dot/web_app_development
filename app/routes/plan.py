from flask import render_template, request, redirect, url_for, flash, session
from app.routes import plan_bp
from app.models.itinerary import Itinerary, ItineraryItem
from app.models.place import Place
from datetime import datetime
import uuid

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入！', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@plan_bp.route('/')
@login_required
def list_itineraries():
    itineraries = Itinerary.query.filter_by(user_id=session['user_id']).order_by(Itinerary.created_at.desc()).all()
    return render_template('itineraries/index.html', itineraries=itineraries)

@plan_bp.route('/new', methods=['GET'])
@login_required
def new_itinerary():
    return render_template('itineraries/new.html')

@plan_bp.route('/', methods=['POST'])
@login_required
def create_itinerary():
    title = request.form.get('title')
    description = request.form.get('description')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    
    if not title or not start_date_str or not end_date_str:
        flash('標題與日期為必填欄位！', 'danger')
        return redirect(url_for('plan.new_itinerary'))
        
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    
    if end_date < start_date:
        flash('結束日期不能早於開始日期！', 'danger')
        return redirect(url_for('plan.new_itinerary'))
        
    share_code = str(uuid.uuid4())[:8]
        
    itinerary = Itinerary.create(
        user_id=session['user_id'],
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        share_code=share_code
    )
    
    flash('行程建立成功！', 'success')
    return redirect(url_for('plan.itinerary_detail', itinerary_id=itinerary.id))

@plan_bp.route('/<int:itinerary_id>')
@login_required
def itinerary_detail(itinerary_id):
    itinerary = Itinerary.get_by_id(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return "找不到該行程", 404
        
    return render_template('itineraries/detail.html', itinerary=itinerary)

@plan_bp.route('/<int:itinerary_id>/edit', methods=['GET'])
@login_required
def edit_itinerary(itinerary_id):
    itinerary = Itinerary.get_by_id(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return "找不到該行程", 404
    return render_template('itineraries/edit.html', itinerary=itinerary)

@plan_bp.route('/<int:itinerary_id>/update', methods=['POST'])
@login_required
def update_itinerary(itinerary_id):
    itinerary = Itinerary.get_by_id(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return "找不到該行程", 404
        
    title = request.form.get('title')
    description = request.form.get('description')
    is_shared = request.form.get('is_shared') == 'on'
    
    if not title:
        flash('標題為必填！', 'danger')
        return redirect(url_for('plan.edit_itinerary', itinerary_id=itinerary.id))
        
    itinerary.update(title=title, description=description, is_shared=is_shared)
    flash('行程更新成功！', 'success')
    return redirect(url_for('plan.itinerary_detail', itinerary_id=itinerary.id))

@plan_bp.route('/<int:itinerary_id>/delete', methods=['POST'])
@login_required
def delete_itinerary(itinerary_id):
    itinerary = Itinerary.get_by_id(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return "找不到該行程", 404
        
    itinerary.delete()
    flash('行程已刪除！', 'success')
    return redirect(url_for('plan.list_itineraries'))

@plan_bp.route('/<int:itinerary_id>/items/new', methods=['GET'])
@login_required
def new_itinerary_item(itinerary_id):
    itinerary = Itinerary.get_by_id(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return "找不到該行程", 404
    
    places = Place.get_all()
    return render_template('itineraries/items_new.html', itinerary=itinerary, places=places)

@plan_bp.route('/<int:itinerary_id>/items', methods=['POST'])
@login_required
def create_itinerary_item(itinerary_id):
    itinerary = Itinerary.get_by_id(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return "找不到該行程", 404
        
    day_number = request.form.get('day_number')
    place_id = request.form.get('place_id')
    expected_cost = request.form.get('expected_cost') or 0
    note = request.form.get('note')
    
    if not day_number:
        flash('天數為必填欄位！', 'danger')
        return redirect(url_for('plan.new_itinerary_item', itinerary_id=itinerary.id))
        
    p_id = int(place_id) if place_id else None
    
    ItineraryItem.create(
        itinerary_id=itinerary.id,
        place_id=p_id,
        day_number=int(day_number),
        expected_cost=float(expected_cost),
        note=note
    )
    
    flash('活動項目新增成功！', 'success')
    return redirect(url_for('plan.itinerary_detail', itinerary_id=itinerary.id))

@plan_bp.route('/<int:itinerary_id>/items/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_itinerary_item(itinerary_id, item_id):
    itinerary = Itinerary.get_by_id(itinerary_id)
    if not itinerary or itinerary.user_id != session['user_id']:
        return "找不到該行程", 404
        
    item = ItineraryItem.query.get(item_id)
    if item and item.itinerary_id == itinerary.id:
        item.delete()
        flash('活動項目已刪除！', 'success')
        
    return redirect(url_for('plan.itinerary_detail', itinerary_id=itinerary.id))
