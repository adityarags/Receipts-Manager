from .database import db

class Organization(db.Model):
    __tablename__ = "organization"
    org_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    Name = db.Column(db.String)
    orgcode = db.Column(db.String)
    Address = db.Column(db.String)
    Phone_Number = db.Column(db.Integer)
    Email = db.Column(db.String)
    PAN = db.Column(db.String)
    Purposes = db.Column(db.String)
    t_no = db.Column(db.String)
    s_no = db.Column(db.String)
    atgr_no = db.Column(db.String)
    aa12_no = db.Column(db.String)
    website = db.Column(db.String)


class Receipt(db.Model):
    __tablename__ = "receipt"
    rid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    org_id = db.Column(db.Integer)
    receipt_date = db.Column(db.String)
    book_no = db.Column(db.Integer)
    receipt_no = db.Column(db.Integer)
    name = db.Column(db.String)
    address = db.Column(db.String)
    state = db.Column(db.String)
    pincode = db.Column(db.Integer)
    landline = db.Column(db.Integer)
    phoneno = db.Column(db.Integer)
    email = db.Column(db.String)
    id_type = db.Column(db.String)
    panid = db.Column(db.String)
    purpose = db.Column(db.String)
    amount = db.Column(db.Integer)
    mode = db.Column(db.String)
    realization_date = db.Column(db.String)

class Donator(db.Model):
    __tablename__ = "donator"
    did = db.Column(db.Integer, primary_key = True, autoincrement = True)
    donator_id = db.Column(db.String)
    org_id = db.Column(db.Integer)
    name = db.Column(db.String)
    address = db.Column(db.String)
    state = db.Column(db.String)
    pincode = db.Column(db.Integer)
    landline = db.Column(db.Integer)
    phoneno = db.Column(db.Integer) 
    email = db.Column(db.String)
    id_type = db.Column(db.String)
    panid = db.Column(db.String)


class Maintainer(db.Model):
    __tablename__ = "maintainer"
    mid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    org_id = db.Column(db.Integer)
    name = db.Column(db.String)

class Book_Maintainers(db.Model):
    __tablename__ = "book_maintainers"
    book_no = db.Column(db.Integer, primary_key = True)
    mid = db.Column(db.Integer)

class Narration(db.Model):
    __tablename__ = "narration"
    nid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    rid = db.Column(db.Integer)
    narration = db.Column(db.String)    