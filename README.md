🏨 StayEase Luxury Hotel Management System
StayEase is a high-end, full-stack hotel booking platform built with Django. It features a sleek user interface, advanced room filtering, real-time booking logic, and professional PDF receipt generation.

🔥 Key Features
Smart Room Discovery: Filter rooms by category (AC, Deluxe, King), capacity, and a dynamic price slider.

"Last Minute Deal" Logic: Automatic visual badges for rooms priced under $100.

Booking Engine: Conflict-preventing booking logic that ensures no double-bookings.

User Dashboard: A "My Bookings" portal where users can track history, cancel stays, and download receipts.

PDF Receipts: On-the-fly PDF generation using xhtml2pdf for confirmed bookings.

Review System: Verified guest reviews with star ratings and featured testimonials on the home page.

Manager Dashboard: A staff-only analytical view to track revenue, total bookings, and room status.

Layer,Technology
Backend,Python / Django 5.x
Frontend,"Bootstrap 5, Animate.css, Google Fonts"
Database,SQLite (Development) / PostgreSQL (Production)
PDF Engine,xhtml2pdf
Icons,Bootstrap Icons



need python 3.14

setup venv

python -m venv venv

activte

./venv/Scripts/activate

then install the requirment in the requirment file

pip install -r requirements.txt
