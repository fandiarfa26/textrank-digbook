from flask import render_template, request, url_for, redirect, send_file
from config import BASE_DIR, UPLOAD_DIR
from app import app
from app.models import Book, Chapter, Summary
from app.add_data import insert_book, insert_chapter
from app.process import get_result

@app.route('/')
@app.route('/index')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/form')
def form():
    books = Book.query.all()
    return render_template('form.html', books=books)

@app.route('/book/add', methods=['POST'])
def addBook():
    title = request.form['title']
    cover = request.files['cover']
    insert_book(title, cover)
    return redirect(url_for('form'))

@app.route('/chapter/add', methods=['POST'])
def addChapter():
    book_id = request.form['choose_book']
    title = request.form['title']
    pdf_ori = request.files['pdf_ori']
    pdf_clean = request.files['pdf_clean']
    insert_chapter(book_id, title, pdf_ori, pdf_clean)
    return redirect(url_for('form'))

@app.route('/result', methods=['POST'])
def result():
    ch_id = request.form['chapter']
    result = get_result(ch_id)
    return render_template('result.html', book_title=result[0], ch_title=result[1], pdf_ori_path=result[2], summary=result[3], keywords=result[4])

@app.route('/uploads/cover_book/<file>')
def return_cover(file):
    try:
        return send_file( UPLOAD_DIR + "cover_book/" + file, attachment_filename=file)
    except Exception as e:
        return str(e)
    
@app.route('/uploads/book/<book>/<file>')
def return_book(book, file):
    try:
        return send_file( UPLOAD_DIR + "book/" + book + "/" + file, attachment_filename=file)
    except Exception as e:
        return str(e)
		
@app.route('/about')
def about():
    return render_template('about.html')