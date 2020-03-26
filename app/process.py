import os
import time
import PyPDF2
from config import UPLOAD_DIR
from app import app, db
from app.models import Book, Chapter, Summary
from app.textrank_summarize import get_summary
from app.textrank_keyword import get_keywords

def extract_text_from_pdf_file(book_code, chapter_code):
    # get file
    i_file = open(os.path.join(UPLOAD_DIR, "book", book_code, chapter_code + ".pdf"), 'rb')
    # create a pdf reader
    pdfReader = PyPDF2.PdfFileReader(i_file)
    # get number of pages
    totalNumPages = pdfReader.numPages
    # get text
    fulltext = ''
    for p in range(0, totalNumPages):
        pageObj = pdfReader.getPage(p)
        fulltext += pageObj.extractText()
    
    return fulltext.replace('\n', '').replace('  ', ' ')

def get_result(ch_id):
    start_time = time.time()
    # Get info from database
    summ_book   = Summary.query.filter_by(chapter_id=ch_id).first()
    the_chapter = Chapter.query.filter_by(id=ch_id).first()
    the_book    = Book.query.filter_by(id=the_chapter.book_id).first()
    # get pdf ori path
    pdf_ori_path = the_book.code + "/" + the_chapter.code + "_ori.pdf"
    # Check if this chapter has been summarized
    if summ_book is None:
        # calculate with Textrank
        fulltext = extract_text_from_pdf_file(the_book.code, the_chapter.code)
        summary = get_summary(fulltext)
        keywords = get_keywords(' '.join(summary))

        str_summary = ";;".join(summary)
        str_keywords = ";".join(keywords)
        newSumm = Summary(text=str_summary, keywords=str_keywords, chapter_id=ch_id)
        db.session.add(newSumm)
        db.session.commit()
    else:
        # get from database
        summary = summ_book.text.split(";;")
        keywords = summ_book.keywords.split(';')

    finish_time = time.time() - start_time
    return [the_book.title, the_chapter.title, pdf_ori_path, summary, keywords]

    
