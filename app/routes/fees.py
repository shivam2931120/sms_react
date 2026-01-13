from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from app.models import Fee, Student
from app import db
from fpdf import FPDF
import io

fees_bp = Blueprint('fees', __name__, url_prefix='/fees')

@fees_bp.route('/pay/<int:fee_id>', methods=['POST'])
@login_required
def pay_fee(fee_id):
    fee = Fee.query.get_or_404(fee_id)
    # Simulate payment logic
    fee.status = 'Paid'
    fee.paid_date = db.func.now()
    db.session.commit()
    flash('Fee paid successfully', 'success')
    return redirect(url_for('student.dashboard'))

@fees_bp.route('/receipt/<int:fee_id>')
@login_required
def download_receipt(fee_id):
    fee = Fee.query.get_or_404(fee_id)
    if fee.status != 'Paid':
        flash('Fee not paid yet', 'warning')
        return redirect(url_for('student.dashboard'))
        
    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Fee Receipt", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Student: {fee.student.first_name}", ln=1)
    pdf.cell(200, 10, txt=f"Amount: ${fee.amount}", ln=1)
    pdf.cell(200, 10, txt=f"Date: {fee.paid_date}", ln=1)
    
    # Save to buffer
    buffer = io.BytesIO()
    s = pdf.output(dest='S').encode('latin-1')
    buffer.write(s)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f'receipt_{fee.id}.pdf', mimetype='application/pdf')
