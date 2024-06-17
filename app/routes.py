from flask import Blueprint, request, jsonify, render_template
from .database import get_db, parse_imdb_page
import random

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return "Scrap IMDB", 200

@routes.route('/review', methods=['POST'])
def add_review():
    db = get_db()
    cursor = db.cursor()
    
    try:
        url = request.json['url']
        rating = request.json['rating']
        review = request.json['review']
        user_id = request.json['user_id']
        username = request.json['username']
        
        if rating < 1 or rating > 10:
            return jsonify({'error': 'La note doit être en 1 et 10.'}), 400
        if len(review) > 500:
            return jsonify({'error': 'Pas plus de 500 signes.'}), 400

        data = parse_imdb_page(url)

        cursor.execute('SELECT * FROM infos WHERE imdbID = ? AND user_id = ?', (data['imdbID'], user_id))
        existing_review = cursor.fetchone()
        
        if existing_review:
            cursor.execute('''
                UPDATE infos
                SET rating = ?,
                    review = ?
                WHERE imdbID = ? AND user_id = ?
            ''', (rating, review, data['imdbID'], user_id))
            db.commit()
            return jsonify({'status': 'success', 'message': 'Ta critique a été modifié.'}), 200
        else:
            cursor.execute('''
                INSERT INTO infos (imdbID, title, year, rating, review, user_id, username)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['imdbID'], data['title'], data['year'], rating, review, user_id, username))
            db.commit()
            return jsonify({'status': 'success', 'message': 'Ta critique est ajoutée.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes.route('/random_review', methods=['POST'])
def random_review():
    db = get_db()
    cursor = db.cursor()
    
    try:
        url = request.json['url']
        data = parse_imdb_page(url)
        
        cursor.execute('SELECT title, review FROM infos WHERE imdbID = ?', (data['imdbID'],))
        reviews = cursor.fetchall()

        if not reviews:
            return jsonify({'error': 'Je trouve rien.'}), 404

        title, review = random.choice(reviews)
        return jsonify({ 'title': title, 'review': review}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/list_reviews', methods=['POST'])
def list_reviews():
    db = get_db()
    cursor = db.cursor()
    
    try:
        url = request.json['url']
        data = parse_imdb_page(url)
        
        cursor.execute('SELECT id, title, rating, username FROM infos WHERE imdbID = ?', (data['imdbID'],))
        reviews = cursor.fetchall()

        if not reviews:
            return jsonify({'error': 'Je trouve rien.'}), 404

        reviews_list = [{'id': review[0], 'title': review[1], 'rating': review[2], 'username': review[3]} for review in reviews]
        return jsonify({'reviews': reviews_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/delete/<int:id>', methods=['DELETE'])
def delete_info(id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute('DELETE FROM infos WHERE id = ?', (id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Not found'}), 404

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@routes.route('/infos')
def infos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM infos')
    infos = cursor.fetchall()

    infos_list = []
    for info in infos:
        infos_list.append({
            'id': info[0],
            'imdbID': info[1],
            'title': info[2],
            'year': info[3],
            'rating': info[4],
            'review': info[5],
            'user_id': info[6],
            'username': info[7]
        })

    return render_template('infos.html', infos=infos_list)
