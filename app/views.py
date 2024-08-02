from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql

main_bp = Blueprint('main', __name__)

# Initialize the limiter
limiter = Limiter(
    key_func=get_remote_address,
    app=current_app,
    storage_uri=f"redis://localhost:6379/0"  # Use the Redis URI directly
)

@main_bp.route('/', methods=['GET'])
def index():
    """Display the form for submitting code snippets and list all snippets."""
    connection = current_app.config['DB_CONNECTION']
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, title FROM code_snippets ORDER BY created_at DESC")
        snippets = cursor.fetchall()

    return render_template('index.html', snippets=snippets)

@main_bp.route('/submit', methods=['POST'])
@limiter.limit("5 per minute")  # Apply rate limiting to form submissions
def submit():
    """Handle form submission and save new code snippet to the database."""
    title = request.form.get('title')
    code = request.form.get('code')

    if title and code:
        connection = current_app.config['DB_CONNECTION']
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO code_snippets (title, code) VALUES (%s, %s)",
                (title, code)
            )
            connection.commit()

    return redirect(url_for('main.index'))

@main_bp.route('/snippet/<int:snippet_id>', methods=['GET'])
def view_snippet(snippet_id):
    """Display a specific code snippet by its ID."""
    connection = current_app.config['DB_CONNECTION']
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT title, code FROM code_snippets WHERE id = %s", (snippet_id,))
        snippet = cursor.fetchone()

    if snippet:
        return render_template('snippet.html', title=snippet['title'], code=snippet['code'])
    else:
        return "Snippet not found", 404
