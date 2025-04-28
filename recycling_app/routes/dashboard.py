from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, cast, Date
from app import db
from models.bottle import BottleScan

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Calculate some basic stats for the user
    total_bottles = current_user.total_bottles
    total_points = current_user.total_points
    rewards_claimed = current_user.rewards_claimed
    
    # Get recycling points from config
    from app import app
    recycling_points = app.config['RECYCLING_POINTS']
    maps_api_key = app.config['GOOGLE_MAPS_API_KEY']
    
    return render_template(
        'dashboard/index.html',
        total_bottles=total_bottles,
        total_points=total_points,
        rewards_claimed=rewards_claimed,
        recycling_points=recycling_points,
        maps_api_key=maps_api_key
    )

@dashboard_bp.route('/stats/weekly')
@login_required
def weekly_stats():
    # Get bottle scans for the last 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)
    
    # Query to get counts by day
    results = db.session.query(
        cast(BottleScan.created_at, Date).label('date'),
        func.count(BottleScan.id).label('count')
    ).filter(
        BottleScan.user_id == current_user.id,
        cast(BottleScan.created_at, Date) >= start_date,
        cast(BottleScan.created_at, Date) <= end_date
    ).group_by(
        cast(BottleScan.created_at, Date)
    ).all()
    
    # Format the data for Chart.js
    dates = []
    counts = []
    
    # Initialize with zeros
    for i in range(7):
        day = start_date + timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d'))
        counts.append(0)
    
    # Fill in actual data
    for result in results:
        day_index = (result.date - start_date).days
        if 0 <= day_index < 7:
            counts[day_index] = result.count
    
    return jsonify({
        'labels': dates,
        'datasets': [{
            'label': 'Bottles Recycled',
            'data': counts,
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    })

@dashboard_bp.route('/stats/materials')
@login_required
def material_stats():
    # Query to get counts by material type
    results = db.session.query(
        BottleScan.material_type,
        func.count(BottleScan.id).label('count')
    ).filter(
        BottleScan.user_id == current_user.id
    ).group_by(
        BottleScan.material_type
    ).all()
    
    # Format the data for Chart.js
    labels = []
    data = []
    
    for result in results:
        labels.append(result.material_type)
        data.append(result.count)
    
    # Color scheme for pie chart
    background_colors = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)'
    ]
    
    border_colors = [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)'
    ]
    
    return jsonify({
        'labels': labels,
        'datasets': [{
            'data': data,
            'backgroundColor': background_colors[:len(data)],
            'borderColor': border_colors[:len(data)],
            'borderWidth': 1
        }]
    })

@dashboard_bp.route('/claim-reward', methods=['POST'])
@login_required
def claim_reward():
    success = current_user.claim_reward()
    
    if success:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Reward claimed successfully!', 'total_points': current_user.total_points})
    else:
        return jsonify({'success': False, 'message': 'Not enough points to claim a reward'})