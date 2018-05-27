# coding: utf-8

__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2018, Paul Cunningham'

from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_select2 import Select2
from flask_select2.model.fields import AjaxSelectField, AjaxSelectMultipleField
from flask_select2.contrib.sqla.ajax import QueryAjaxModelLoader


app = Flask(__name__)
bootstrap = Bootstrap(app)
select2 = Select2()

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

db = SQLAlchemy(app)


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(255), nullable=False)
    description = db.Column(db.UnicodeText(), nullable=True)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name


company_loader = QueryAjaxModelLoader(
    name='company',
    session=db.session,
    model=Company,
    fields=['name'],
    order_by=[Company.name.asc()],
    page_size=20,
    placeholder="Select a company"
)

select2.init_app(app)
select2.add_loader(loader=company_loader)


class CompanyForm(FlaskForm):

    single_company = AjaxSelectField(
        loader=company_loader,
        label='Single Company',
        allow_blank=False
    )

    multiple_company = AjaxSelectMultipleField(
        loader=company_loader,
        label='Multiple Companies',
        allow_blank=False
    )

    single_company_allow_blank = AjaxSelectField(
        loader=company_loader,
        label='Single Company (blank allowed)',
        allow_blank=True,
    )


# Flask views
@app.route('/', methods=['GET', 'POST'])
def index():
    _form = CompanyForm()

    if _form.validate_on_submit():

        flash("Single Company selected : {name}".format(name=_form.single_company.data.name), category='success')

        flash("Multiple Companies selected : {names}".format(names=','.join(c.name for c in _form.multiple_company.data)), category='success')

        if _form.single_company_allow_blank.data:

            flash("Single Company (blank allowed) selected : {name}".format(name=_form.single_company.data.name), category='success')
        else:
            flash("Single Company (blank allowed) nothing selected.", category='danger')

    return render_template('index.html', form=_form)


@app.before_first_request
def build_sample_db():

    db.drop_all()
    db.create_all()

    fake = Faker()

    # add 2000 companies
    db.session.bulk_insert_mappings(
        Company,
        [
            dict(
                name=fake.company(),
                description=fake.paragraph(nb_sentences=fake.random.randint(1, 10))
            )
            for _ in range(2000)
        ]
    )

    db.session.commit()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
