from flask import render_template, request, redirect, url_for, send_file, flash
from flask import current_app as app
from .database import db
from .models import Organization, Receipt, Donator, Maintainer, Book_Maintainers, Narration
from sqlalchemy import func, or_, and_
import numpy as np
import pandas as pd
from fileinput import filename

DF = None
CURRENT_NARRATION = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/createOrganization", methods = ["GET", "POST"])
def createOrg():
    if request.method == "GET":
        return render_template("createOrg.html")
    elif request.method == "POST":
        newOrg = Organization(
            orgcode = request.form["orgcode"],
            Name = request.form["name"],
            Address = request.form["address"],
            Phone_Number = request.form["phone"],
            Email = request.form["email"],
            PAN = request.form["pan"],
            t_no = request.form["trustno"],
            s_no = request.form["societyno"],
            atgr_no = request.form["atgregno"],
            aa12_no = request.form["12aano"],
            website = request.form["website"],
            Purposes = ""
        )
        
        db.session.add(newOrg)
        db.session.commit()
       
        return render_template("createOrg.html")


@app.route("/selectOrganization")
def orgSelect():
    allorganizations = Organization.query.all()
    return render_template("organizationSelect.html", allorganizations = allorganizations)


@app.route("/Organization/<int:org_id>")
def orgDashboard(org_id):
    current_org = Organization.query.filter_by(org_id = org_id).all()
    print(current_org)
    return render_template("dashboard.html", Organization = current_org[0])


@app.route("/<int:org_id>/receipt", methods = ["GET", "POST"])
def receipt(org_id):
    if request.method == "POST":
        newReceipt = Receipt(
            org_id = org_id,
            book_no = request.form["bno"],
            receipt_no = request.form["rno"],
            receipt_date = request.form["rdate"],
            name = request.form["name"],
            address = request.form["address"],
            state = request.form["state"],
            pincode = request.form["pincode"],
            landline = request.form["landline"],
            phoneno = request.form["phone"],
            email = request.form["email"],
            id_type = request.form["id_type"],
            panid = request.form["pan"],
            purpose = request.form["purposes"],
            amount = request.form["amount"],
            mode = request.form["mode"],
            realization_date = ""
        )

        db.session.add(newReceipt)
        db.session.commit()

        current_org = Organization.query.filter_by(org_id = org_id).all()[0]
        purposes = current_org.Purposes.split(",")
        return render_template("receipt.html", purposes = purposes, org = current_org)
    
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    purposes = current_org.Purposes.split(",")
    return render_template("receipt.html", purposes = purposes, org = current_org)


@app.route("/updateReceipt/<int:rid>/", methods = ["GET", "POST"])
def updateReceipt(rid):
    currentReceipt = Receipt.query.filter_by(rid = rid).all()[0]
    org_id = currentReceipt.org_id
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    purposes = current_org.Purposes.split(",")
    if request.method == "POST":
        if request.form["rdate"] != "":
            currentReceipt.receipt_date = request.form["rdate"]
        if request.form["bno"] != "":
            currentReceipt.book_no = request.form["bno"]
        if request.form["rno"] != "":
            currentReceipt.receipt_no = request.form["rno"]
        if request.form["name"] != "":
            currentReceipt.name = request.form["name"]
        if request.form["address"] != "":
            currentReceipt.address = request.form["address"]
        if request.form["state"] != "":
            currentReceipt.state = request.form["state"]
        if request.form["pincode"] != "":
            currentReceipt.pincode = request.form["pincode"]
        if request.form["landline"] != "":
            currentReceipt.landline = request.form["landline"]
        if request.form["phone"] != "":
            currentReceipt.phoneno = request.form["phone"]
        if request.form["email"] != "":
            currentReceipt.email = request.form["email"]
        
        if request.form["id_type"] != "":
            currentReceipt.id_type = request.form["id_type"]

        if request.form["purposes"] != "":
            currentReceipt.purpose = request.form["purposes"]
        
        if request.form["pan"] != "":
            currentReceipt.panid = request.form["pan"]

        
        if request.form["amount"] != "":
            currentReceipt.amount = request.form["amount"]
        
        if request.form["mode"] != "":
            currentReceipt.mode = request.form["mode"]
        db.session.commit()
    return render_template("updateReceipt.html", receipt = currentReceipt, purposes = purposes, org_id = org_id    )

@app.route("/<int:org_id>/addPurpose", methods = ["GET", "POST"])
def addPurpose(org_id):

    if request.method == "POST":

        current_org = Organization.query.filter_by(org_id = org_id).all()[0]
        purposes = current_org.Purposes.split(",")
        if not request.form["purpose"].isspace() and request.form["purpose"] != "":
            purposes.append(request.form["purpose"])

        updatedPurposes = ",".join(purposes)
        current_org.Purposes = updatedPurposes
        db.session.commit()

        return render_template("addPurposes.html", purposes = purposes, org = current_org)

    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    purposes = current_org.Purposes.split(",")
    return render_template("addPurposes.html", purposes = purposes, org = current_org)




@app.route("/deletepurpse/<int:org_id>/<purpose>")
def delete_purpose(org_id, purpose):
    in_use_purposes = db.session.query(
        Receipt.purpose,
    ).filter_by(org_id = org_id).all()

    in_use_purposes = [_[0] for _ in in_use_purposes]

    if not purpose in in_use_purposes:
        current_org = Organization.query.filter_by(org_id = org_id).all()[0]
        purposes = current_org.Purposes.split(",")
        purposes.remove(purpose)

        updatedPurposes = ",".join(purposes)
        current_org.Purposes = updatedPurposes
        db.session.commit()

        return redirect(url_for("addPurpose", org_id = org_id))


    return redirect(url_for("addPurpose", org_id = org_id))


@app.route("/deletepurpse/<int:org_id>/")
def delete_purpose_blank(org_id):
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    purposes = current_org.Purposes.split(",")
    purposes.remove("")

    updatedPurposes = ",".join(purposes)
    current_org.Purposes = updatedPurposes
    db.session.commit()
    return redirect(url_for("addPurpose", org_id = org_id))


@app.route("/<int:org_id>/donatorList")
def donators(org_id):
    
    donators = db.session.query(
        Receipt.name,
        func.sum(Receipt.amount).label('Amount'),
        Receipt.panid,
        Receipt.phoneno
    ).filter_by(org_id = org_id).group_by(Receipt.panid).all()
    return render_template("donators.html", donators = donators, org_id = org_id)


@app.route("/<int:org_id>/checkData")
def transactions(org_id):
    receipts = Receipt.query.filter_by(org_id = org_id).all()
    return render_template("allData.html", receipts = receipts, org_id = org_id)


@app.route("/download/<int:org_id>")
def downloadFile(org_id):
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    receipts = Receipt.query.filter_by(org_id = org_id).all()
    alldata = []
    for _ in receipts:
        alldata.append((_.receipt_date, _.book_no, _.receipt_no, _.name, _.address, _.state, _.pincode, _.landline, 
        _.phoneno, _.email, _.id_type, _.panid, _.purpose, _.amount, _.mode, _.realization_date))
    df = pd.DataFrame(alldata , columns =["Receipt Date", "Book Number", "Receipt Number", "Name", "Address", "State", "Pin Code", "Landline Number", "Phone Number", "Email ID", "ID Number", "PAN ID", "Purpose", "Amount", "Mode", "Realization Date"])
    df.replace("",np.NaN)

    df.to_excel(f"app_data/{current_org.Name}_transactions.xlsx", index = False)
    print(df.head())
    return send_file(f"app_data/{current_org.Name}_transactions.xlsx")

@app.route("/<int:org_id>/frequentDonator", methods = ["GET", "POST"])
def frequentDonator(org_id):
    if request.method == "POST":

        newDonator = Donator(
            org_id = org_id,
            name = request.form["name"],
            address = request.form["address"],
            state = request.form["state"],
            pincode = request.form["pincode"],
            landline = request.form["landline"],
            phoneno = request.form["phone"], 
            email = request.form["email"],
            id_type = request.form["id_type"],
            panid = request.form["pan"]
        )

        db.session.add(newDonator)
        current_org = Organization.query.filter_by(org_id = org_id).all()[0]
        newDonator.donator_id = current_org.orgcode + str(newDonator.did)
        db.session.commit()

    return render_template("frequentdonator.html", org_id = org_id)


@app.route("/<int:org_id>/listFreqDonators", methods = ["GET", "POST"])
def listFreqDonators(org_id):
    all_donators = Donator.query.filter_by(org_id = org_id).all()
    if request.method == "POST":
        keyword = request.form["search"]
        all_donators = db.session.query(Donator).filter(or_(Donator.name.like(f"%{keyword}%"), Donator.phoneno.like(f"%{keyword}%"), Donator.donator_id.like(f"%{keyword}%"))).all()


    return render_template("listFreqDonators.html", org_id = org_id, all_donators = all_donators)

@app.route("/<int:org_id>/downloadFrequentDonator/")
def downloadFrequentDonator(org_id):
    return send_file("app_data/Sample Donator Master File.xlsx")

@app.route("/<int:org_id>/uploadFrequentDonator/", methods = ["GET", "POST"])
def uploadFrequentDonator(org_id):
    if request.method == "POST":
        f = request.files["file"]
        df = pd.read_excel(f, names = ["name", "address", "state", "pincode", "landline", "phoneno", "email","id_type", "panid"])
        curr_orgcode = Organization.query.filter_by(org_id = org_id)[0].orgcode
        offset = Donator.query.all()[-1].did
        df["org_id"] = np.array([org_id] * df.shape[0])
        df = df.fillna("")
        # id_offsets = np.array(map(str, range(Donator.query.all()[-1].did + 1, Donator.query.all()[-1].did + 1 + df.shape[0])))
        
        df = df.drop_duplicates(subset=['panid'])
        df["donator_id"] = np.char.add(np.array([curr_orgcode] * df.shape[0]).astype(str), np.array(list(range(offset + 1, offset + 1 + df.shape[0]))).astype(str))
        df.to_sql(name='donator', con=db.engine, index=False, if_exists = "append")
        print(df.head(10))
        
        
    return render_template("uploadDonator.html", org_id = org_id)
    

@app.route('/<int:org_id>/<int:did>/generateReceipt', methods = ["GET", "POST"])
def generateDonatorReceipt(org_id, did):
    if request.method == "POST":
        current_donator = Donator.query.filter_by(did = did).all()[0]
        
        newReceipt = Receipt(
            org_id = org_id,
            book_no = request.form["bno"],
            receipt_no = request.form["rno"],
            receipt_date = request.form["rdate"],
            name = current_donator.name,
            address = current_donator.address,
            state = current_donator.state,
            pincode = current_donator.pincode,
            landline = current_donator.landline,
            phoneno = current_donator.phoneno,
            email = current_donator.email,
            id_type = current_donator.id_type,
            panid = current_donator.panid,
            purpose = request.form["purposes"],
            amount = request.form["amount"],
            mode = request.form["mode"],
            realization_date = ""
        )

        db.session.add(newReceipt)
        db.session.commit()
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    purposes = current_org.Purposes.split(",")
    return render_template("DonatorReceipt.html", purposes = purposes, org_id = org_id, did = did)

@app.route("/<int:org_id>/uploadTransactions", methods = ["GET", "POST"])
def uploadTransactions(org_id):
    if request.method == "POST":
        f = request.files["file"]
        df = pd.read_excel(f, names = ["receipt_date", "book_no", "receipt_no", "name", "address", 
        "state", "pincode", "landline", "phoneno", "email","id_type", "panid", "purpose", "amount", "mode", "realization_date"])
        
        df["org_id"] = [org_id] * df.shape[0]
        df = df.fillna("")
        df["book_no"] = df["book_no"].replace("", 0).astype(int)
        df["receipt_no"] = df["receipt_no"].replace("", 0).astype(int)
        df["amount"] = df["amount"].replace("", 0).astype(int)

        print(df.head())
        global DF
        DF = df

        # df.to_sql(name='receipt', con=db.engine, index=False, if_exists = "append")
        # db.session.commit()
        return redirect(url_for("uploadCheck", org_id = org_id))




    return render_template("uploadTransactions.html", org_id = org_id)

@app.route("/<int:org_id>/uploadCheck", methods = ["GET", "POST"])
def uploadCheck(org_id):
    global DF
    if request.method == "POST":
        DF.to_sql(name='receipt', con=db.engine, index=False, if_exists = "append")
        db.session.commit()
        DF = None
        return redirect(url_for("orgDashboard", org_id = org_id))
    avail_pans = [_[0] for _ in db.session.query(Donator.panid).distinct(Donator.panid).filter_by(org_id = org_id).all()]
    uniquePans = DF[~DF.panid.isin(avail_pans)]
    # uniquePans = uniquePans[uniquePans.panid != ""]
    uniquePans = uniquePans.drop_duplicates(subset=['panid'])
    current_purposes = list(np.unique(DF["purpose"]))
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    avail_purposes = current_org.Purposes.split(",")
    uniquePurposes = [_ for _ in current_purposes if _ not in avail_purposes]
    uniquePans = uniquePans.replace("", " ")
    uniquePans = uniquePans.reset_index()
    for i in range(uniquePans.shape[0]):
        print(uniquePans["name"][i])
    return render_template("uploadCheck.html", uniquePans = uniquePans, uniquePurposes = uniquePurposes, org_id = org_id)



@app.route("/<int:org_id>/addUniquePurpose/<purpose>")
def addUniquePurpose(org_id, purpose):
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    purposes = current_org.Purposes.split(",")
    purposes        .append(purpose)
    updatedPurposes = ",".join(purposes)
    current_org.Purposes = updatedPurposes
    db.session.commit()
    return redirect(url_for("uploadCheck", org_id = org_id))

@app.route("/<int:org_id>/addUniqueDonator/<name>/<address>/<state>/<pincode>/<landline>/<phoneno>/<email>/<id_type>/<panid>")
def addUniqueDonator(org_id, name, address, state, pincode, landline, phoneno, email, id_type ,panid):
    newDonator = Donator(
        org_id = org_id,
        name = name,
        address = address,
        state = state,
        pincode = pincode,
        landline = landline,
        id_type = id_type,
        phoneno = phoneno, 
        email = email,
        panid = panid
    )

    db.session.add(newDonator)
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    newDonator.donator_id = current_org.orgcode + str(newDonator.did)
    db.session.commit()
    return redirect(url_for("uploadCheck", org_id = org_id))

@app.route("/generateReport/<int:org_id>/<int:mid>", methods = ["GET", "POST"])
def generateReport(org_id, mid):
    details = []
    if request.method == "POST":

        managed_books = [_[0] for _ in db.session.query(Book_Maintainers.book_no).filter(Book_Maintainers.mid == mid).all()]

        receipts = [_ for _ in Receipt.query.filter_by(org_id = org_id).all() if _.book_no in managed_books]
        selected = request.form["column"]
        alldata = []
        for _ in receipts:
            alldata.append((_.receipt_date, _.book_no, _.receipt_no, _.name, _.address, _.state, _.pincode, _.landline, 
            _.phoneno, _.email, _.panid, _.purpose, _.amount, _.mode, _.realization_date))
            df = pd.DataFrame(alldata , columns = ["receipt_date", "book_no", "receipt_no", "name", "address", 
        "state", "pincode", "landline", "phoneno", "email", "panid", "purpose", "amount", "mode", "realization_date"])
        
        details = [(df["name"][_], df["address"][_] + "," + df["state"][_] + "," + str(df["pincode"][_]), df["landline"][_] , df["phoneno"][_], df["receipt_no"][_]) for _ in range(df.shape[0]) if df[selected][_] in [0, "", None, np.nan] or str(df[selected][_]).isspace()]
        downlaodFile = pd.DataFrame(details, columns = ["Name", "Address", "Landline Number", "Mobile Number", "Receipt Number"])
        downlaodFile.to_csv("app_data/report_download.csv", index = False)
    return render_template("report.html", org_id = org_id, details = details)

@app.route("/<int:org_id>/NarrationUpdate", methods = ["GET", "POST"])
def NarrationUpdate(org_id):
    receipts = []
    if request.method == "POST":
        if request.form["options"] == "Cash":
            receipts = [_ for _ in db.session.query(Receipt).filter(and_(Receipt.mode == "Cash", Receipt.org_id == org_id)).all() if _.rid not in [__.rid for __ in Narration.query.all()]]
        elif request.form["options"] == "Others":
            receipts = [_ for _ in db.session.query(Receipt).filter(and_(Receipt.mode != "Cash", Receipt.org_id == org_id)).all() if _.rid not in [__.rid for __ in Narration.query.all()]]
    return render_template("narrationUpdate.html", org_id = org_id, receipts = receipts)


@app.route("/narrationUpdate/<int:org_id>/<int:rid>", methods = ["GET", "POST"])
def updateNarrationVals(org_id, rid):
    if request.method == "POST":
        realization_date = str(request.form["realization_date"])
        newNarration = Narration(rid = rid, narration = request.form["narration"])
        db.session.add(newNarration)
        curr_receipt = db.session.query(Receipt).filter(and_(Receipt.rid == rid, Receipt.org_id == org_id)).all()[0]
        curr_receipt.realization_date = realization_date
        db.session.commit()
        return redirect(url_for("NarrationUpdate", org_id = org_id))
    return render_template("narrationValsUpdate.html", org_id = org_id)
@app.route("/reportDownload")
def downloadReport():
    return send_file("app_data/report_download.csv")
@app.route("/downloadTemplate")
def downloadTemplate():
    return send_file("app_data/Sample Transactions File.xlsx")

@app.route("/<int:org_id>/bookMaintainers", methods = ["GET", "POST"])
def bookMaintainers(org_id):
    if request.method == "POST":
        newMaintainer = Maintainer(org_id = org_id, 
        name = request.form["name"])
        db.session.add(newMaintainer)
        db.session.commit()
    maintainers = Maintainer.query.filter_by(org_id = org_id).all()
    current_org = Organization.query.filter_by(org_id = org_id).all()[0]
    return render_template("bookMaintainers.html", org = current_org, maintainers = maintainers)


@app.route("/assignBook/<int:org_id>/<int:mid>")
def assignBook(org_id, mid):
    org_books = db.session.query(Receipt.book_no).distinct(Receipt.book_no).filter_by(org_id = org_id)
    assignedBooks = db.session.query(Book_Maintainers.book_no)
    available_books = [book[0] for book in org_books if book not in assignedBooks]

    return render_template("assignBook.html", org_id = org_id , mid = mid, books = available_books)

@app.route("/assignBook/assigned/<int:org_id>/<int:book_no>/<int:mid>")
def bookAssigned(org_id, book_no, mid):
    newAssign = Book_Maintainers(book_no = book_no, mid = mid)
    db.session.add(newAssign)
    db.session.commit()
    return redirect(url_for("assignBook", org_id = org_id, mid = mid))

@app.route("/<org_id>/NarrationReport", methods = ["GET", "POST"])
def narrationReport(org_id):
    receipts = []
    if request.method == "POST":
        narrations = Narration.query.all()
        if request.form["options"] == "Cash":
            receipts = [_ for _ in db.session.query(Receipt).filter(and_(Receipt.mode == "Cash", Receipt.org_id == org_id)).all() if _.rid in [__.rid for __ in narrations]]
        elif request.form["options"] == "Others":
            receipts = [_ for _ in db.session.query(Receipt).filter(and_(Receipt.mode != "Cash", Receipt.org_id == org_id)).all() if _.rid in [__.rid for __ in narrations]]
    mapping = {receipts[_]: db.session.query(Narration).filter(Narration.rid == receipts[_].rid).all()[0] for _ in range(len(receipts))}
    global CURRENT_NARRATION
    CURRENT_NARRATION = mapping
    return render_template("narrationReport.html", mapping = mapping, org_id = org_id, )

@app.route("/downlaodCurrentNarrationReport")
def downlaodCurrentNarrationReport():
    with open("app_data/NarrationReport.txt", "w") as f:
        lines = []
        for i in CURRENT_NARRATION:
            lines.append(str(i.receipt_no) + "/" + str(i.amount) + "/" + str(i.realization_date) + "/" + str(CURRENT_NARRATION[i].narration) + "/" + str(i.panid))
        f.writelines(lines)
    return send_file("app_data/NarrationReport.txt", as_attachment = True)