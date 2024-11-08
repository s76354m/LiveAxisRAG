from flask import Blueprint, render_template, request, jsonify
from src.forms.competitor import CompetitorEntryForm
from src.services.timer import TimerService
from src.services.office365 import Office365Service

competitor_bp = Blueprint('competitor', __name__)
timer_service = TimerService()
o365_service = Office365Service()

@competitor_bp.route('/competitor/entry', methods=['GET', 'POST'])
def competitor_entry():
    form = CompetitorEntryForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            competitor = Competitor(
                project_id=form.project_id.data,
                product=form.product.data
            )
            db.session.add(competitor)
            db.session.commit()
            
            # Start progress timer (maps to PowerApps Timer1)
            timer_service.start_timer(
                'progress_update',
                5000,  # 5 seconds
                lambda: update_progress(competitor.id)
            )
            
            return jsonify({'status': 'success'})
            
    return render_template(
        'competitor_entry.html',
        form=form
    ) 