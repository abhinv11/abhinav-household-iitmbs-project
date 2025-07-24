# Household Services Management System (Complete full Stack app)

A comprehensive web application for managing household services, connecting customers with professional service providers. This Flask-based application provides a complete platform for booking, managing, and reviewing household services.

## 🚀 Features

### For Customers
- **User Registration & Authentication**: Secure signup and login system
- **Service Discovery**: Browse and search available household services
- **Professional Selection**: View and select from approved service professionals
- **Service Booking**: Schedule services with preferred professionals
- **Request Management**: Edit, track, and manage service requests
- **Review System**: Rate and review completed services
- **Complaint Filing**: File complaints for unsatisfactory services

### For Service Professionals
- **Professional Registration**: Register with service specialization and documents
- **Profile Management**: Manage professional profile and availability
- **Request Handling**: Accept or reject service requests
- **Status Updates**: Update service completion status
- **Document Upload**: Upload verification documents for approval

### For Administrators
- **Service Management**: Add, edit, and delete service categories
- **Professional Approval**: Review and approve professional registrations
- **User Management**: Block/unblock customers and professionals
- **System Oversight**: Monitor all platform activities and complaints

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Authentication**: Session-based authentication
- **File Handling**: Document upload and storage

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.7 or higher
- pip (Python package installer)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd abhinav-household-iitmbs-project-main
   ```

2. **Navigate to the project directory**
   ```bash
   cd household_services_project
   ```

3. **Install required dependencies**
   ```bash
   pip install flask flask-sqlalchemy
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## 🗃️ Database Schema

The application uses the following main entities:

- **User**: Base user entity with roles (Admin, Customer, Professional)
- **Customer**: Customer-specific information (address, pincode)
- **Professional**: Professional details (service, experience, documents)
- **Service**: Available service categories
- **ServiceRequest**: Service booking requests
- **Review**: Customer reviews and ratings
- **Complaint**: Customer complaints

## 🚪 Default Login Credentials

### Administrator Access
- **Email**: admin@gmail.com
- **Password**: admin123

## 📁 Project Structure

```
household_services_project/
├── app.py                      # Main application file
├── backend/
│   ├── models.py              # Database models
│   └── controllers.py         # Route handlers and business logic
├── templates/                 # HTML templates
│   ├── admin_*.html          # Admin interface templates
│   ├── customer_*.html       # Customer interface templates
│   ├── professional_*.html   # Professional interface templates
│   └── *.html               # Common templates
├── static/
│   ├── styles/              # CSS stylesheets
│   └── uploads/             # Uploaded documents
└── instance/
    └── household_services.sqlite3  # SQLite database
```

## 🔄 Application Workflow

1. **Registration**: Users register as customers or professionals
2. **Approval**: Administrators approve professional registrations
3. **Service Discovery**: Customers browse available services
4. **Booking**: Customers book services with professionals
5. **Service Delivery**: Professionals accept and complete requests
6. **Review**: Customers rate completed services
7. **Management**: Administrators oversee the entire process

## 🔐 User Roles & Permissions

### Admin
- Manage all services and categories
- Approve/block professionals
- Monitor user activities
- Handle complaints and disputes

### Customer
- Book and manage service requests
- Rate and review services
- File complaints
- Edit personal information

### Professional
- Manage service requests
- Update availability status
- View earnings and ratings
- Upload verification documents

## 🚀 Getting Started

1. Start the application using `python app.py`
2. Register as a customer or professional
3. If registering as a professional, wait for admin approval
4. Browse services and start booking!

## 📞 Support

For any issues or questions, please refer to the application's built-in complaint system or contact the system administrator.

## 📄 License

This project is developed as part of an academic assignment for IIT Madras BS program.

---

**Note**: This is a educational project designed to demonstrate web application development concepts including user management, service booking systems, and multi-role authentication.
