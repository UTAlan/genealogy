from app import app
from flask import flash, redirect, render_template, request, url_for
import os
from app.spouse_relative_checker import run_checker
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'ged'}

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/spouse-relative-checker', methods=['GET', 'POST'])
def spouse_relative_checker():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    
    file = request.files['file']
    
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)

    if file and allowed_file(file.filename):
      # Save the uploaded file
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)
      
      # Run the checker!
      results = run_checker(file_path)
      
      # Delete the uploaded file
      os.remove(file_path)
      
      # Output results to the screen
      return results
    
    return 'Invalid file. Make sure the file ends in .ged and try again.'

  return render_template('spouse_relative_checker.html')