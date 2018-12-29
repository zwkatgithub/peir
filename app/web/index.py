from flask import render_template, session, redirect, url_for
from app.web import web
from app.helpers.index_helper import format_topics, choice2str
from app.forms.set_pn import PNForm
from app.forms.search_form import SearchForm



@web.route('/', methods=['get','post'])
def index():
    if not hasattr(session, 'last'):
        session['last'] = 10
    form = PNForm(n=session['last'])
    search = SearchForm()
    print(search.disease.data, search.gene.data, search.type_.data)
    if search.validate_on_submit():
        print("here")
        url = '/search/user/{disease}/{gene}/{n}/{type_}'.format(
            disease=search.disease.data, gene=search.gene.data, n=session['last'],type_=choice2str(search.type_.data)
        )
        return redirect(url)
    if form.validate_on_submit():
        session['last'] = form.n.data


    res = format_topics(form.n.data)
    return render_template('index.html', topics=res, n=form.n.data, form=form, search=search)
