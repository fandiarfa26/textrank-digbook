import random
import string
import os
from flask import url_for, redirect
from app import db
from config import UPLOAD_DIR
from app.models import Book, Chapter

def insert_book(title, cover):
    code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    ext = cover.filename.split('.')[-1]
    cover.save(UPLOAD_DIR + 'cover_book/' + code+'.'+ext)
    os.makedirs(UPLOAD_DIR + 'book/' + code)
    newBook = Book(code=code, title=title)
    db.session.add(newBook)
    db.session.commit()

def insert_chapter(book_id, title, pdf_ori, pdf_clean):
    the_book = Book.query.filter_by(id=book_id).first()
    code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
    pdf_ori.save(UPLOAD_DIR + 'book/' + the_book.code + '/' + code + '_ori.pdf')
    pdf_clean.save(UPLOAD_DIR + 'book/' + the_book.code + '/' + code + '.pdf')
    newChapter = Chapter(code=code, title=title, book_id=book_id)
    db.session.add(newChapter)
    db.session.commit()