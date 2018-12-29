from flask import render_template, request

from app.forms.search_form import SearchForm
from app.web import web
from app.helpers.search_helper import format_results
from ir.search import Search
from ir.config import RETURN_SIZE
from app.models.result import Record
from ir.result import Result


@web.route('/search/<int:topic>/<int:n>')
def search_tpoic(topic, n = RETURN_SIZE):
    s = Search(topic)
    records = Record.records(topic, n)
    if len(records) != 0:
        results = [Result(record.doc_id, record.score) for record in records]
    else:
        results = s.search()
        records = [Record(pn=n, topic_id=topic, score=result.score, doc_id=result.doc_id) for result in results]
        Record.save_all(records)
    p = s.p(results, n)
    res = format_results(topic, results, n, p)
    return render_template('search_result.html',n=n, p=p, results=res)

@web.route('/search/user/<string:disease>/<string:gene>/<int:n>/<string:type_>')
def search_by_user(disease, gene, n, type_):
    s = Search()
    results = s.search_by_user(disease, gene, type_)
    #p = s.p(results, n)
    res = format_results(None, results, n, p=None)
    return render_template("search_result.html", n=n, p=False, results=res)