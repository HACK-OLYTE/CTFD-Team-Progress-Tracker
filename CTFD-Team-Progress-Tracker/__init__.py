from flask import Blueprint, render_template, jsonify, request
from CTFd.utils.decorators import admins_only
from CTFd.models import db, Teams, Challenges, Solves, Submissions
from CTFd.utils import get_config
from sqlalchemy import func
import json


def load(app):
    team_progress = Blueprint(
        'team_progress', 
        __name__, 
        template_folder='templates', 
        static_folder='assets',
        url_prefix='/plugins/team-progress'
    )
   
    @team_progress.route('/admin/team_progress')
    @admins_only
    def admin_view():
        """Page principale d'administration du plugin"""
        teams = Teams.query.all()
        return render_template('team_progress.html', teams=teams)
   
    @team_progress.route('/admin/team_progress/api/teams')
    @admins_only
    def get_teams():
        """API pour récupérer la liste des équipes"""
        teams = Teams.query.filter(Teams.banned == False).all()
        return jsonify([{
            'id': team.id,
            'name': team.name
        } for team in teams])
   
    def get_challenge_requirements(challenge):
        """Extrait les prérequis d'un challenge"""
        try:
            if isinstance(challenge.requirements, str):
                reqs = json.loads(challenge.requirements) if challenge.requirements else {}
            else:
                reqs = challenge.requirements or {}
            
            if isinstance(reqs, dict) and 'prerequisites' in reqs:
                prerequisites = reqs['prerequisites']
                # Valider que c'est une liste d'entiers
                if isinstance(prerequisites, list):
                    return [int(req_id) for req_id in prerequisites if isinstance(req_id, (int, str)) and str(req_id).isdigit()]
                return []
            return []
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            # Logger l'erreur au lieu de la masquer silencieusement
            print(f"⚠️ Erreur parsing requirements pour challenge {challenge.id}: {e}")
            return []
    
    def is_challenge_unlocked(challenge_id, solved_challenges, all_challenges_req):
        """Vérifie si un challenge est débloqué selon ses prérequis"""
        if challenge_id not in all_challenges_req:
            return True  # Pas de prérequis = toujours accessible
        
        requirements = all_challenges_req[challenge_id]
        if not requirements:
            return True  # Liste vide = accessible
        
        # Tous les prérequis doivent être résolus
        return all(req_id in solved_challenges for req_id in requirements)
   
    @team_progress.route('/admin/team_progress/api/team/<int:team_id>')
    @admins_only
    def get_team_progress(team_id):
        """API pour récupérer la progression d'une équipe avec gestion des prérequis"""
        
        # Vérifier que l'équipe existe et n'est pas bannie
        team = Teams.query.filter_by(id=team_id, banned=False).first()
        if not team:
            return jsonify({'error': 'Team not found'}), 404
    
        # Récupérer tous les challenges visibles avec leurs requirements
       
        # Récupérer tous les challenges visibles avec leurs requirements
        challenges = db.session.query(
            Challenges.id,
            Challenges.name,
            Challenges.category,
            Challenges.value,
            Challenges.requirements
        ).filter(Challenges.state == 'visible').all()
       
        # Créer un mapping des requirements par challenge
        all_challenges_req = {}
        for challenge in challenges:
            all_challenges_req[challenge.id] = get_challenge_requirements(challenge)
       
        # Grouper par catégorie
        categories = {}
        for challenge in challenges:
            if challenge.category not in categories:
                categories[challenge.category] = []
            categories[challenge.category].append({
                'id': challenge.id,
                'name': challenge.name,
                'value': challenge.value,
                'requirements': all_challenges_req[challenge.id]
            })
       
        # Récupérer les solves de l'équipe
        team_solves = db.session.query(
            Solves.challenge_id,
            Solves.date
        ).filter(Solves.team_id == team_id).all()
       
        solved_challenges = {solve.challenge_id for solve in team_solves}
        solved_challenges_dates = {solve.challenge_id: solve.date.isoformat() for solve in team_solves}
       
        # Récupérer les tentatives de l'équipe
        team_attempts = db.session.query(
            Submissions.challenge_id,
            func.count(Submissions.id).label('attempts')
        ).filter(
            Submissions.team_id == team_id
        ).group_by(Submissions.challenge_id).all()
       
        attempts_count = {attempt.challenge_id: attempt.attempts for attempt in team_attempts}
       
        # Construire la réponse avec le statut de chaque challenge
        result = {}
        for category, challs in categories.items():
            result[category] = []
            for chall in challs:
                challenge_id = chall['id']
                attempts = attempts_count.get(challenge_id, 0)
                is_unlocked = is_challenge_unlocked(challenge_id, solved_challenges, all_challenges_req)
                
                # Déterminer le statut selon la nouvelle logique
                if challenge_id in solved_challenges:
                    status = 'solved'
                    solve_date = solved_challenges_dates[challenge_id]
                elif not is_unlocked:
                    status = 'locked'  # Non débloqué
                    solve_date = None
                elif attempts > 0:
                    status = 'attempted'  # Accessible et tenté
                    solve_date = None
                else:
                    status = 'accessible'  # Accessible mais pas tenté
                    solve_date = None
                
                # Récupérer les noms des prérequis pour l'affichage
                req_names = []
                if chall['requirements']:
                    req_challenges = db.session.query(Challenges.name).filter(
                        Challenges.id.in_(chall['requirements'])
                    ).all()
                    req_names = [req.name for req in req_challenges]
               
                result[category].append({
                    'id': challenge_id,
                    'name': chall['name'],
                    'value': chall['value'],
                    'status': status,
                    'attempts': attempts,
                    'solve_date': solve_date,
                    'requirements': req_names,  # Noms des challenges requis
                    'is_unlocked': is_unlocked
                })
       
        return jsonify(result)
   
    # Route pour le menu admin plugins
    @app.route('/admin/plugins/CTFD-Team-Progress-Tracker')
    @admins_only
    def admin_team_progress():
        """Route accessible depuis le menu plugins de l'admin"""
        return render_template('team_progress.html')
   
    app.register_blueprint(team_progress)