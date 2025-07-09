WorkDocX is a feature-rich dashboard and admin template that offers a vast collection of UI elements, components, widgets, and pages to help you build web applications quickly and efficiently. Its clean and adaptable layout is fully customizable, making it the ideal choice for developers and designers who want to save time and create high-quality solutions for their clients. Whether you’re building custom admin panels, dashboards, CRMs, CMSs, e-commerce panels, or other types of web applications, WorkDocX has got you covered.

Features:
Built using the latest bootstrap (v5.3.3)
Easy customizations with extensive use of SCSS variables
Fully responsive and works across all modern/supported browsers, devices
Documentation on all available components, widgets, etc
Easy development and tooling with Gulp workflow
Landing Page included

Multiple Demos/Layout Options:
WorkDocX provides three pre-built layout options and a flexible layout system to cater to the needs of modern web applications. Its ready-to-use UI elements and build automation using gulp-based tools enable developers to create web applications quickly and efficiently.

Components:
All Bootstrap components
Icons
Multiple widgets
Toast Notifications
Charts included using Chart.js, Brite Charts, and Apex
Select2, Date Range Picker, Input Mask included
Bootstrap form wizard
Time Picker
Spinner
Max Length Validator
Advanced Datatables
Dragula – Simple Drag and Drop
Multiple File Uploads
WYSIWYG Editors (Quill Js and SimpleMDE)
Google and Vector Maps
Layouts:
Vertical Layout (With different sidebar themes including default, light, dark, etc)
Horizontal Layout
Detached Sidebar Layout
Boxed (Fixed width) for Vertical and Horizontal
Apps:
Calendar
Projects (List page, Detail Page, Create Project Page, Gantt)
Tasks (List Page, Detail Modal, Add Task Modal, Kanban Board)
Ecommerce (Product listing, product detail, order listing, order detail, shopping cart, checkout, seller listing, etc)
Email (Inbox, Email details page, compose, etc)
Chat
Social Feed
File Manager
Pages:
Sample Dashboards
Profile
Invoice
FAQ
Timeline
Pricing
Maintenance
Login (Two variations)
Register (Two variations)
Logout (Two variations)
Recover Password (Two variations)
Lock Screen (Two variations)
Confirm Mail (Two variations)
Error 404
Error 500

├── config
│   ├── settings
│   │    ├── base.py
│   │    ├── local.py
│   │    └── production.py
│   └── urls.py - all the urls
├── WorkDocX
│   ├── static
│   │   ├── css
│   │   ├── fonts
│   │   ├── images
│   │   ├── js
│   │   └── scss
│   ├── templates
│   │   └── all the html pages
│   └── all the django apps
├── requirements
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── utility
├── bun.lockb
├── db.sqlite3
├── gulpfile.js
├── manage.py
├── package-lock.json
├── package.json
└── yarn.lock


pip install --no-deps --upgrade-strategy only-if-needed -r requirements/local.txt


