#App routes
from flask import Flask, render_template,request, url_for, redirect,session,flash
from .models import *
from flask import current_app as app
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import current_app


@app.route("/")
def home():
    return render_template("index.html")

#-----------login Routes--------------------
@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        uname = request.form.get("user_mail")
        pwd = request.form.get("password")
        usr = User.query.filter_by(email=uname, password=pwd).first()

        if usr:
            if not usr.is_active:  # Check if the user is active
                return render_template("login.html", msg="Your account is blocked. Please contact support.")

            if usr.role == UserRole.ADMIN:  # If exists and is admin
                return redirect(url_for("admin_dashboard", name=uname))
            
            elif usr.role == UserRole.CUSTOMER:  # If exists and is customer
                customer = Customer.query.filter_by(user_id=usr.id).first()
                if not customer:
                    return render_template("login.html", msg="Customer details not found!")
                return redirect(url_for("user_dashboard", customer_id=customer.customer_id, name=uname))
            
            elif usr.role == UserRole.PROFESSIONAL:  # If exists and is professional
                professional = Professional.query.filter_by(user_id=usr.id).first()
                if not professional.is_approved:
                    return render_template("login.html", msg="Your account is awaiting admin approval.")
                return redirect(url_for("professional_dashboard", name=uname, professional_id=professional.professional_id))
        
        # Invalid credentials
        return render_template("login.html", msg="Invalid User Credentials")
    
    return render_template("login.html", msg="")


#--------Register Routes for Customer----------------------
@app.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uname = request.form.get("user_mail")
        pwd = request.form.get("password")
        user_name = request.form.get("user_name")
        address = request.form.get("user_address")
        pincode = request.form.get("user_pincode")

        #check if username is already registerd or not
        usr = User.query.filter_by(email = uname).first()
        if usr:
            return render_template("signup.html", msg = "Sorry, this mail is already registerd")

        # Create a new User instance
        new_usr0 = User(email=uname, password=pwd, full_name=user_name)
        db.session.add(new_usr0)
        db.session.flush()  # Ensure the ID is generated

        # Create a new Customer instance linked to the User
        new_usr1 = Customer(user_id=new_usr0.id, address=address, pincode=pincode)
        db.session.add(new_usr1)

        # Commit the transaction
        db.session.commit()
        return render_template("login.html", msg = "Registration Successfull, Please login")

    return render_template("signup.html", msg = "")

#-----------------Register Route for Professioanl---------------
@app.route("/professionalregister", methods=["GET", "POST"])
def professionalsignup():
    services = get_services()
    
    if request.method == "POST":
        uname = request.form.get("user_mail")
        pwd = request.form.get("password")
        user_name = request.form.get("user_name")
        city = request.form.get("city")
        experience = request.form.get("user_exp")
        role = UserRole.PROFESSIONAL
        description = request.form.get("description")
        service_name = request.form.get("service_name")
        is_approved = False  # Default to not approved
        file = request.files.get('formFile')

        # Initialize file_path to None
        file_path = None
            # Define allowed_file function
        def allowed_file(filename):
            ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        # File upload configurations
        UPLOAD_FOLDER = 'static/uploads/documents'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        # Check if a file is uploaded and valid
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create the upload folder if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file_path = os.path.join('uploads/documents', filename).replace("\\", "/")  # Save relative to 'static'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Check if username is already registered
        usr = User.query.filter_by(email=uname).first()
        if usr:
            return render_template("professional_signup.html", msg="Sorry, this mail is already registered", services=services)

        # Create a new User instance
        new_usr0 = User(email=uname, password=pwd, full_name=user_name, role=role)
        db.session.add(new_usr0)
        db.session.flush()  # Ensure the ID is generated

        # Create a new Professional instance linked to the User
        new_usr1 = Professional(
            user_id=new_usr0.id, 
            city=city, 
            experience=experience, 
            description=description, 
            service_id=service_name, 
            document_path=file_path  # None if no file uploaded
        )
        db.session.add(new_usr1)

        # Commit the transaction
        db.session.commit()

        return render_template("login.html", msg="Registration Successful, Please login")

    return render_template("professional_signup.html", msg="", services=services)


#---------------Common Routes--------------------------------------------

#common route for admin dashboard
@app.route("/admin/<name>")
def admin_dashboard(name):
    services = get_services()
    professionals = get_professional_details()
    customers = get_customer_details()
    service_requests = get_service_requests()
    
    return render_template("admin_dashboard.html", name = name, services = services, professionals = professionals, customers = customers, service_requests = service_requests)

# Common route for customer dashboard
@app.route("/customer/<int:customer_id>/<string:name>")
def user_dashboard(customer_id, name):
    # Fetch services available for customers
    services = Service.query.all()  # Query all services (or add a filter based on business logic)
    services1 = get_services_with_professionals()
    # Fetch service requests made by this specific customer
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()

    # Render the dashboard template with the data
    return render_template(
        "customer_dashboard.html",
        name=name,
        services=services,
        service_requests=service_requests,
        customer_id=customer_id,
        service1 = services1
    )


#common route for professional dashboard
@app.route("/professional/<int:professional_id>/<string:name>")
def professional_dashboard(professional_id,name):
    service_requests = ServiceRequest.query.filter_by(professional_id = professional_id).all()
    return render_template("professional_dashboard.html", name = name, service_requests=service_requests)


# ----------------------------Admin Routes---------------------------------

#add_service route for admin
@app.route("/addservice/<name>", methods = ["GET","POST"])
def add_service(name):
    if request.method == "POST":
        s_name = request.form.get("service_name")
        s_description = request.form.get("description")
        min_price = request.form.get("min_price")
        min_time = request.form.get("min_time")

        # Create a new Service instance
        new_service = Service(
            service_name=s_name,
            description=s_description,
            min_price=int(min_price),
            min_time_required=int(min_time)
        )
        # Add to the database session and commit
        db.session.add(new_service)
        db.session.commit()

        return redirect(url_for("admin_dashboard", name = name))




    return render_template("admin_addservice.html", name = name)

#search for admin
@app.route("/search/<name>", methods = ["GET","POST"])
def search(name):
    if request.method == "POST":
        search_txt = request.form.get("search_txt")
        by_service = search_by_service(search_txt)
        by_professional = search_by_professional(search_txt)
        by_customer = search_by_customer(search_txt)

        if by_service:
            return render_template("admin_dashboard.html",name = name, services = by_service)
        elif by_professional:
            return render_template("admin_dashboard.html",name = name, professionals = by_professional)
        elif by_customer:
            return render_template("admin_dashboard.html",name = name, customers = by_customer)
    return redirect(url_for("admin_dashboard", name = name))

#edit service route for admin
@app.route("/edit_service/<service_id>/<name>", methods = ["GET","POST"])
def edit_service(service_id,name):
    s = get_service(service_id)
    if request.method == "POST":
        service_name = request.form.get("service_name")
        description = request.form.get("description")
        min_price = request.form.get("min_price")
        min_time = request.form.get("min_time")
        s.service_name = service_name
        s.description = description
        s.min_price = min_price
        s.min_time = min_time
        db.session.commit()
        return redirect(url_for("admin_dashboard", name = name))
    return render_template("admin_editservice.html", service = s, name = name)

#delete service route for admin
@app.route("/delete_service/<service_id>/<name>", methods = ["GET","POST"])
def delete_service(service_id,name):
    s = get_service(service_id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("admin_dashboard", name = name))

#admin approve 
@app.route("/approve_professional/<int:professional_id>", methods=["GET"])
def approve_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    professional.is_approved = True
    professional.is_active = True
    db.session.commit()
    return redirect(url_for("admin_dashboard", name="Admin"))

@app.route("/block_professional/<int:professional_id>", methods=["GET"])
def block_professional(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    professional.is_approved = False
    professional.is_active = False
    db.session.commit()
    return redirect(url_for("admin_dashboard", name="Admin"))

@app.route('/handle-admin-action/<int:id>/<string:role>', methods=['POST'])
def handle_admin_action(id, role):
    if 'id' not in session or session['role'] != 'ADMIN':
        return redirect(url_for("signin"))

    user = User.query.get(id)
    print("user",user, role)
    if not user:
        return redirect(url_for('admin_dashboard'))
    user.is_active = not user.is_active

    db.session.commit()
    return redirect(url_for('admin_dashboard'))

# function to block Customer
@app.route('/toggle_customer_status/<int:customer_id>', methods=['POST'])
def toggle_customer_status(customer_id):
    # Fetch the customer record by ID
    customer = Customer.query.get(customer_id)

    if customer and customer.user:
        # Toggle the is_active status
        customer.user.is_active = not customer.user.is_active
        db.session.commit()
        action = "blocked" if not customer.user.is_active else "unblocked"
        flash(f"Customer {customer.user.full_name} has been {action}.", "success")
    else:
        flash("Customer not found.", "error")

    # Redirect back to the admin dashboard
    return redirect(url_for('admin_dashboard', name ="admin"))

#-----------------Coutomer Routes--------------------------

#search for customer
@app.route("/search/<customer_id>/<name>", methods=["GET", "POST"])
def search_customer(customer_id, name):
    if request.method == "POST":
        search_txt = request.form.get("search_txt")

        # Fetch results
        by_service = search_by_service(search_txt)  # Services that match the search
        by_service_request = search_by_service_request(search_txt)  # Service requests that match the search

        # Render the template with both results
        return render_template(
            "customer_dashboard.html",
            name=name,
            services=by_service,
            service_requests=by_service_request,
            customer_id=customer_id,
        )
    return redirect(url_for("customer_dashboard", customer_id=customer_id, name=name))


#Routes to book Service for customer
@app.route("/customerbookrequest/<cid>/<sid>/<pid>/<name>", methods=["GET", "POST"])
def customerbookrequest(cid, sid, pid, name):
    if request.method == "POST":
        # Get the preferred date and time from the form
        preferred_datetime = request.form.get("preferred_datetime")
        preferred_datetime = datetime.strptime(preferred_datetime, '%Y-%m-%dT%H:%M')

        # Save the service request to the database
        new_service_request = ServiceRequest(
            customer_id=cid,
            service_id=sid,
            professional_id=pid,
            service_request_time=preferred_datetime,
            status=ServiceRequestStatus.PENDING)
        db.session.add(new_service_request)
        db.session.commit()
    
        # Redirect to the customer dashboard after booking
        return redirect(url_for("user_dashboard", name=name, customer_id=cid))

    service = Service.query.filter_by(service_id=sid).first()
    # Render the booking form
    return render_template(
        "customer_bookservice.html",
        cid=cid,
        sid=sid,
        sname=service.service_name,
        pid=pid,
        name=name
    )

@app.route("/service_professionals/<int:service_id>/<int:customer_id>/<string:name>")
def service_professionals(service_id, customer_id, name):
    # Get professionals for the specific service
    professionals = Professional.query.filter_by(service_id=service_id, is_approved=True).all()
    service = Service.query.get_or_404(service_id)
    
    return render_template(
        "service_professionals.html",
        professionals=professionals,
        service=service,
        customer_id = customer_id,
        name = name)

@app.route("/edit_service_request/<int:service_request_id>/<string:name>", methods=["GET", "POST"])
def edit_service_request(service_request_id, name):
    service_request = ServiceRequest.query.get_or_404(service_request_id)

    # Only allow editing if the status is "Pending"
    if service_request.status != ServiceRequestStatus.PENDING:
        flash("You can only edit requests with 'Pending' status.", "error")
        return redirect(url_for("user_dashboard", customer_id=service_request.customer_id, name=name))

    if request.method == "POST":
        # Get the new time and combine it with the existing date
        new_time = request.form.get("preferred_time")
        new_datetime = f"{service_request.service_request_time.strftime('%Y-%m-%d')} {new_time}"
        service_request.service_request_time = datetime.strptime(new_datetime, '%Y-%m-%d %H:%M')
        db.session.commit()
        flash("Service request time updated successfully.", "success")
        return redirect(url_for("user_dashboard", customer_id=service_request.customer_id, name=name))

    return render_template(
        "edit_service_request.html",
        service_request=service_request,
        name=name
    )


#-------------------Professional routes-----------------
#when professional accepts request
@app.route("/accept_request/<int:service_request_id>")
def accept_request(service_request_id):
    service_request = ServiceRequest.query.get_or_404(service_request_id)
    if service_request.status == ServiceRequestStatus.PENDING:
        service_request.status = ServiceRequestStatus.ACCEPTED
        db.session.commit()
    return redirect(url_for("professional_dashboard", 
                            professional_id=service_request.professional_id, 
                            name=service_request.professional.user.full_name))


#when professional rejects the requests
@app.route("/reject_request/<int:service_request_id>")
def reject_request(service_request_id):
    service_request = ServiceRequest.query.get_or_404(service_request_id)
    if service_request.status == ServiceRequestStatus.PENDING:
        service_request.status = ServiceRequestStatus.CANCELLED
        db.session.commit()
    return redirect(url_for("professional_dashboard", 
                            professional_id=service_request.professional_id, 
                            name=service_request.professional.user.full_name))

#when professional mark request as completed
@app.route("/complete_request/<int:service_request_id>")
def complete_request(service_request_id):
    service_request = ServiceRequest.query.get_or_404(service_request_id)
    if service_request.status == ServiceRequestStatus.ACCEPTED:
        service_request.status = ServiceRequestStatus.COMPLETED
        db.session.commit()
    return redirect(url_for("professional_dashboard", 
                            professional_id=service_request.professional_id, 
                            name=service_request.professional.user.full_name))
#-----------------------------------------------------------------------------------------------------------

#------------Rate and Complaint Routes

@app.route("/rate_service_request/<int:service_request_id>/<string:name>", methods=["GET", "POST"])
def rate_service_request(service_request_id, name):
    service_request = ServiceRequest.query.get_or_404(service_request_id)

    if request.method == "POST":
        rating = int(request.form.get("rating"))
        review_text = request.form.get("review")

        # Create a new Review entry
        new_review = Review(
            service_request_id=service_request.service_request_id,
            professional_id=service_request.professional_id,
            rating=rating,
            review=review_text
        )
        db.session.add(new_review)
        db.session.commit()

        flash("Thank you for your feedback!", "success")
        return redirect(url_for("user_dashboard", customer_id=service_request.customer_id, name=name))

    return render_template("rate_service_request.html", service_request=service_request, name=name)

@app.route("/file_complaint/<int:service_request_id>/<string:name>", methods=["GET", "POST"])
def file_complaint(service_request_id, name):
    service_request = ServiceRequest.query.get_or_404(service_request_id)

    if request.method == "POST":
        complaint_text = request.form.get("complaint")

        # Create a new Complaint entry
        new_complaint = Complaint(
            service_request_id=service_request.service_request_id,
            professional_id=service_request.professional_id,
            description=complaint_text
        )
        db.session.add(new_complaint)
        db.session.commit()

        flash("Your complaint has been submitted.", "success")
        return redirect(url_for("user_dashboard", customer_id=service_request.customer_id, name=name))

    return render_template("file_complaint.html", service_request=service_request, name=name)

#-------------------------------------------------------------------------------
#other supported function
def get_services():
    services = Service.query.all()
    return services

    #function to get professional details
def get_professional_details():
    professionals = Professional.query.all()
    return professionals

    #function to get customer details
def get_customer_details():
    customers = Customer.query.all()
    return customers

    #function to get service_requests
def get_service_requests():
    services_requests = ServiceRequest.query.all()
    return services_requests


    #function to search #-----------
def search_by_service(search_txt):
    services_search = Service.query.filter(Service.service_name.ilike(f"%{search_txt}%")).all()
    return services_search

def search_by_customer(search_txt):
    customers = Customer.query.join(User).filter(User.full_name.ilike(f"%{search_txt}%")).all()
    return customers

def search_by_professional(search_txt):
    professionals = Professional.query.join(User).filter(User.full_name.ilike(f"%{search_txt}%")).all()
    return professionals

    #---------------
def get_service(service_id):
    service = Service.query.filter_by(service_id = service_id).first()
    return service

def search_by_service_request(search_txt):
    # Query the ServiceRequest model and join with the Service model
    services_request_search = (
        ServiceRequest.query
        .join(Service)  # Join ServiceRequest with Service
        .filter(Service.service_name.ilike(f"%{search_txt}%"))  # Filter by service_name
        .all()
    )
    return services_request_search

    

def get_services_with_professionals():
    services = Service.query.all()
    services_with_professionals = []
    for service in services:
        professionals = Professional.query.filter_by(service_id=service.service_id).all()
        services_with_professionals.append({"service": service, "professionals": professionals})
    return services_with_professionals





# @app.route("/block_customer/<int:customer_id>", methods=["GET"])
# def block_customer(customer_id):
#     customer = Customer.query.get_or_404(customer_id)
#     customer.is_active = False
#     db.session.commit()
#     return redirect(url_for("admin_dashboard", name="Admin"))















