from flask import Blueprint, request, jsonify, current_app, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
import base64
from datetime import datetime
import numpy as np
import cv2
from app import db
from models.bottle import BottleScan
from models.user import User
from services.bottle_scan import analyze_bottle_image

bottle_bp = Blueprint('bottle', __name__, url_prefix='/bottle')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bottle_bp.route('/scan', methods=['GET', 'POST'])
@login_required
def scan():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files and 'image_data' not in request.form:
            flash('No file part or image data', 'error')
            return redirect(request.url)
        
        file_path = None
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                # Create a unique filename
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
        
        # Handle webcam image
        elif 'image_data' in request.form:
            image_data = request.form['image_data']
            # Remove data URL prefix
            if 'data:image/' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Save image to file
            filename = str(uuid.uuid4()) + '.jpg'
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
        
        if file_path:
            # Analyze the bottle image using AI model
            result = analyze_bottle_image(file_path)
            
            # Create a new bottle scan record
            bottle_scan = BottleScan(
                user_id=current_user.id,
                image_path=file_path.replace(current_app.config['UPLOAD_FOLDER'], '/static/uploads'),
                is_recyclable=result['is_recyclable'],
                material_type=result['material_type'],
                estimated_value=result['estimated_value']
            )
            
            db.session.add(bottle_scan)
            
            # Update user points and bottle count
            current_user.add_points(bottle_scan.points_earned)
            current_user.add_bottle()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'result': result,
                'points_earned': bottle_scan.points_earned,
                'total_points': current_user.total_points
            })
        
    # GET request - render the scanning page
    return render_template('bottle/scan.html')

@bottle_bp.route('/history')
@login_required
def history():
    # Get user's bottle scan history
    scans = BottleScan.query.filter_by(user_id=current_user.id).order_by(BottleScan.created_at.desc()).all()
    return render_template('bottle/history.html', scans=scans)