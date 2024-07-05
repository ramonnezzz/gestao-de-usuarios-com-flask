from flask import Flask, render_template, request, redirect, url_for
from user import db, User  # Ajuste isso com base na estrutura do seu projeto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Cria as tabelas com base nos modelos
with app.app_context():
    db.create_all()

# Configuração do diretório estático
@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory(app.static_folder, filename)

# Defina suas rotas e lógica de aplicativo aqui
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        telefone = request.form['telefone']
        cpf = request.form['cpf']
        
        new_user = User(username=username, email=email, telefone=telefone, cpf=cpf)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/view-users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('view_users'))


@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.telefone = request.form['telefone']
        user.cpf = request.form['cpf']
        
        db.session.commit()
        return redirect(url_for('view_users'))
    
    return render_template('edit_user.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
