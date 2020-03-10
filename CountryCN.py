#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import json
from app import app
from app import db
from app.models import Country


countries = json.load(io.open("country-code.json"))
for country in countries:
    print(country)
    country_db  = Country.query.get(country['en'])
    if country_db is None:
        country_db = Country(name_EN=country['en'])
        db.session.add(country_db)

    country_db.name_CN  = country['cn']
    db.session.commit()

unTranslated = Country.query.filter(Country.name_CN == None).all()
for country in unTranslated:
    print(country.name_EN)
    cn = input("输入中文:")
    country.name_CN = cn
    db.session.commit()
