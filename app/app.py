import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, jsonify, request
import logging
import sqlite3
import db
import random
import os

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) doenca FROM DOENCAS)
    JOIN
      (SELECT COUNT(*) estatistica FROM ESTATISTICAS)
    JOIN
      (SELECT COUNT(*) faixa FROM FAIXAS_ETARIAS)
    JOIN 
      (SELECT COUNT(*) hospital FROM HOSPITAIS)
    JOIN 
      (SELECT COUNT(*) regiao FROM REGIOES)
    ''').fetchone()
    logging.info(stats)
    return render_template('main.html',stats=stats)

# ---------------------------------- HOSPITAIS --------------------------------------------

@APP.route('/hospitals/')
def list_hospitais():
    hospitals = db.execute(
      '''
      SELECT *
      FROM HOSPITAIS
      ORDER BY hospital_id
      ''').fetchall()
    return render_template('hospital-list.html', hospitals=hospitals)

@APP.route('/hospitals/<int:id>/')
def get_hospital(id):
  hospital = db.execute(
      '''
      SELECT *
      FROM HOSPITAIS 
      WHERE hospital_id = ?
      ''', [id]).fetchone()

  if hospital is None:
     abort(404, 'Hospital id {} does not exist.'.format(id))

  region = db.execute(
      '''
      SELECT r.nome
      FROM HOSPITAIS h
      JOIN REGIOES r
      WHERE hospital_id = ?
      ''', [id]).fetchone()

  diseases = db.execute(
    '''
    SELECT DISTINCT h.nome, d.doenca_id, d.descricao
    FROM HOSPITAIS h
    NATURAL JOIN ESTATISTICAS e
    JOIN DOENCAS d ON d.doenca_id = e.doenca_id
    WHERE h.hospital_id = ?
    ORDER BY d.doenca_id
    ''', [id]).fetchall()

  stats = db.execute(
    '''
    SELECT SUM(e.obitos) as o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM HOSPITAIS h
    JOIN ESTATISTICAS e ON h.hospital_id = e.hospital_id
    WHERE h.hospital_id = ?
    ''', [id]).fetchone()
  
  periodo = db.execute(
    '''
    SELECT e.periodo, SUM(e.obitos) as o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM HOSPITAIS h
    JOIN ESTATISTICAS e ON h.hospital_id = e.hospital_id
    WHERE h.hospital_id = ?
    GROUP BY e.periodo
    ''', [id]).fetchall()
  
  genero = db.execute(
    '''
    SELECT g.genero AS g, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM HOSPITAIS h
    JOIN ESTATISTICAS e ON h.hospital_id = e.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    WHERE h.hospital_id = ?
    GROUP BY g.genero
    ''', [id]).fetchall()

  faixa = db.execute(
    '''
    SELECT CONCAT(f.idade_min, "-", f.idade_max) AS age_range, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM HOSPITAIS h
    JOIN ESTATISTICAS e ON h.hospital_id = e.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    JOIN FAIXAS_ETARIAS f ON g.faixa_etaria_id = f.faixa_etaria_id
    WHERE h.hospital_id = ?
    GROUP BY g.faixa_etaria_id
    ''', [id]).fetchall()
  
  ambos = db.execute(
    '''
    SELECT CONCAT(f.idade_min, "-", f.idade_max) AS age_range, g.genero, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM HOSPITAIS h
    JOIN ESTATISTICAS e ON h.hospital_id = e.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    JOIN FAIXAS_ETARIAS f ON g.faixa_etaria_id = f.faixa_etaria_id
    WHERE h.hospital_id = ?
    GROUP BY g.faixa_etaria_id, g.genero
    ORDER BY g.genero
    ''', [id]).fetchall()
  
  return render_template('hospital.html', hospital=hospital, region=region, diseases=diseases, stats=stats, periodo=periodo, genero=genero, faixa=faixa, ambos=ambos)

@APP.route('/hospitals/<int:id_h>/<int:id_d>/')
def get_hospital_disease(id_h, id_d):
  stats = db.execute(
      '''
      SELECT DISTINCT d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, SUM(obitos) as o, SUM(ambulatorio) as a, SUM(internamentos) as i
      FROM DOENCAS d
      JOIN ESTATISTICAS e ON d.doenca_id = e.doenca_id
      JOIN HOSPITAIS h on h.hospital_id = e.hospital_id
      JOIN REGIOES r on r.regiao_id = h.regiao_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      ''', [id_d, id_h]).fetchone()

  if stats is None:
     abort(404, 'Stats id {} does not exist.'.format(id))

  genero = db.execute(
      '''
      SELECT p.genero, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, SUM(obitos) as o, SUM(ambulatorio) as a, SUM(internamentos) as i
      FROM DOENCAS d
      JOIN ESTATISTICAS e ON d.doenca_id = e.doenca_id
      JOIN HOSPITAIS h ON h.hospital_id = e.hospital_id
      JOIN REGIOES r ON r.regiao_id = h.regiao_id
      JOIN GRUPOS p ON p.paciente_id = e.paciente_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      GROUP BY p.genero
      ''', [id_d, id_h]).fetchall()

  faixa = db.execute(
      '''
      SELECT CONCAT(idade_min, '-', idade_max) AS age_range, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, SUM(obitos) as o, SUM(ambulatorio) as a, SUM(internamentos) as i
      FROM DOENCAS d
      JOIN ESTATISTICAS e ON d.doenca_id = e.doenca_id
      JOIN HOSPITAIS h ON h.hospital_id = e.hospital_id
      JOIN REGIOES r ON r.regiao_id = h.regiao_id
      JOIN GRUPOS p ON p.paciente_id = e.paciente_id
      JOIN FAIXAS_ETARIAS f ON p.faixa_etaria_id = f.faixa_etaria_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      GROUP BY p.faixa_etaria_id
      ''', [id_d, id_h]).fetchall()

  ambos = db.execute(
      '''
      SELECT CONCAT(idade_min, '-', idade_max) AS age_range, p.genero, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, SUM(obitos) as o, SUM(ambulatorio) as a, SUM(internamentos) as i
      FROM DOENCAS d
      JOIN ESTATISTICAS e ON d.doenca_id = e.doenca_id
      JOIN HOSPITAIS h ON h.hospital_id = e.hospital_id
      JOIN REGIOES r ON r.regiao_id = h.regiao_id
      JOIN GRUPOS p ON p.paciente_id = e.paciente_id
      JOIN FAIXAS_ETARIAS f ON p.faixa_etaria_id = f.faixa_etaria_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      GROUP BY p.faixa_etaria_id, p.genero
      ORDER BY p.genero
      ''', [id_d, id_h]).fetchall()

  periodo = db.execute(
      '''
      SELECT e.periodo, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, SUM(obitos) as o, SUM(ambulatorio) as a, SUM(internamentos) as i
      FROM DOENCAS d
      JOIN ESTATISTICAS e ON d.doenca_id = e.doenca_id
      JOIN HOSPITAIS h ON h.hospital_id = e.hospital_id
      JOIN REGIOES r ON r.regiao_id = h.regiao_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      GROUP BY e.periodo
      ''', [id_d, id_h]).fetchall()
      
  
  return render_template('hospital-disease.html', stats=stats, genero=genero, faixa=faixa, ambos=ambos, periodo=periodo)


# -------------------------------------------------- REGIOES ------------------------------------------

@APP.route('/regions/')
def list_regions():
    regions = db.execute(
      '''
      SELECT *
      FROM REGIOES
      ORDER BY regiao_id
      ''').fetchall()
    return render_template('region-list.html', regions=regions)

@APP.route('/regions/<int:id>/')
def get_region(id):
  stats = db.execute(
      '''
      SELECT r.regiao_id, r.nome, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
      FROM REGIOES r
      JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
      JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
      WHERE r.regiao_id = ?
      ''', [id]).fetchone()

  diseases = db.execute(
    '''
    SELECT DISTINCT d.doenca_id, d.descricao
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN DOENCAS d ON d.doenca_id = e.doenca_id
    WHERE r.regiao_id = ?
    ORDER BY d.doenca_id
    ''', [id]).fetchall()
  
  periodo = db.execute(
    '''
    SELECT e.periodo, SUM(e.obitos) as o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    WHERE r.regiao_id = ?
    GROUP BY e.periodo
    ''', [id]).fetchall()
  
  genero = db.execute(
    '''
    SELECT g.genero AS g, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    WHERE r.regiao_id = ?
    GROUP BY g.genero
    ''', [id]).fetchall()

  faixa = db.execute(
    '''
    SELECT CONCAT(f.idade_min, "-", f.idade_max) AS age_range, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    JOIN FAIXAS_ETARIAS f ON g.faixa_etaria_id = f.faixa_etaria_id
    WHERE r.regiao_id = ?
    GROUP BY g.faixa_etaria_id
    ''', [id]).fetchall()
  
  ambos = db.execute(
    '''
    SELECT CONCAT(f.idade_min, "-", f.idade_max) AS age_range, g.genero, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    JOIN FAIXAS_ETARIAS f ON g.faixa_etaria_id = f.faixa_etaria_id
    WHERE r.regiao_id = ?
    GROUP BY g.faixa_etaria_id, g.genero
    ORDER BY g.genero
    ''', [id]).fetchall()
  
  if not stats or not diseases or not periodo or not genero or not faixa or not ambos:
    return "Dados insuficientes para exibir esta página", 404

  
  return render_template('region.html', diseases=diseases, stats=stats, periodo=periodo, genero=genero, faixa=faixa, ambos=ambos)

@APP.route('/regions/<int:r_id>/<int:d_id>')
def get_region_disease(r_id, d_id):
  stats = db.execute(
      '''
      SELECT r.regiao_id, r.nome, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i, e.doenca_id, d.descricao
      FROM REGIOES r
      JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
      JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
      JOIN DOENCAS d on d.doenca_id = e.doenca_id
      WHERE r.regiao_id = ? and e.doenca_id = ?
      ''', [r_id, d_id]).fetchone()

  diseases = db.execute(
    '''
    SELECT DISTINCT d.doenca_id, d.descricao
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN DOENCAS d ON d.doenca_id = e.doenca_id
    WHERE r.regiao_id = ? and e.doenca_id = ?
    ORDER BY d.doenca_id
    ''', [r_id,d_id]).fetchall()
  
  periodo = db.execute(
    '''
    SELECT e.periodo, SUM(e.obitos) as o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    WHERE r.regiao_id = ? and e.doenca_id = ?
    GROUP BY e.periodo
    ''', [r_id, d_id]).fetchall()
  
  genero = db.execute(
    '''
    SELECT g.genero AS g, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    WHERE r.regiao_id = ? and e.doenca_id = ?
    GROUP BY g.genero
    ''', [r_id, d_id]).fetchall()

  faixa = db.execute(
    '''
    SELECT CONCAT(f.idade_min, "-", f.idade_max) AS age_range, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    JOIN FAIXAS_ETARIAS f ON g.faixa_etaria_id = f.faixa_etaria_id
    WHERE r.regiao_id = ? and e.doenca_id = ?
    GROUP BY g.faixa_etaria_id
    ''', [r_id, d_id]).fetchall()
  
  ambos = db.execute(
    '''
    SELECT CONCAT(f.idade_min, "-", f.idade_max) AS age_range, g.genero, SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i
    FROM REGIOES r
    JOIN HOSPITAIS h ON h.regiao_id = r.regiao_id
    JOIN ESTATISTICAS e ON e.hospital_id = h.hospital_id
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    JOIN FAIXAS_ETARIAS f ON g.faixa_etaria_id = f.faixa_etaria_id
    WHERE r.regiao_id = ? and e.doenca_id = ?
    GROUP BY g.faixa_etaria_id, g.genero
    ORDER BY g.genero
    ''', [r_id, d_id]).fetchall()
  
  if not stats or not diseases or not periodo or not genero or not faixa or not ambos:
    return "Dados insuficientes para exibir esta página", 404

  
  return render_template('region-disease.html', diseases=diseases, stats=stats, periodo=periodo, genero=genero, faixa=faixa, ambos=ambos)

# ------------------------------------------------- DOENCAS

@APP.route('/diseases/')
def list_diseases():
    diseases = db.execute(
      '''
      SELECT *
      FROM DOENCAS
      ORDER BY doenca_id
      ''').fetchall()
    return render_template('doenca-list.html', diseases=diseases)

@APP.route('/diseases/<int:id>/')
def get_disease(id):
    count = db.execute(
      '''
      SELECT SUM(e.obitos) AS o, SUM(e.ambulatorio) AS a, SUM(e.internamentos) AS i, d.doenca_id, d.descricao
      FROM DOENCAS d
      NATURAL JOIN ESTATISTICAS e
      WHERE d.doenca_id = ?
      ''', [id]).fetchone()
    
    regions = db.execute(
      '''
      SELECT r.regiao_id, r.nome
      FROM DOENCAS
      NATURAL JOIN ESTATISTICAS 
      NATURAL JOIN REGIOES r
      WHERE doenca_id = ?
      GROUP BY nome
      ORDER BY r.regiao_id
      ''', [id]).fetchall()

    hospitals = db.execute(
      '''
      SELECT h.hospital_id, h.nome
      FROM DOENCAS
      NATURAL JOIN ESTATISTICAS
      NATURAL JOIN HOSPITAIS h
      WHERE doenca_id = ?
      GROUP BY nome
      ORDER BY h.hospital_id
      ''', [id]).fetchall()
    
    return render_template('doenca.html', count=count, regions=regions, hospitals=hospitals)

def get_random_color():
    """Generates a random RGBA color for datasets."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgba({r}, {g}, {b}, 0.2)", f"rgba({r}, {g}, {b}, 1)"  # Background and border colors


@APP.route('/radar-data')
def radar_data():
    # Connect to your database
    conn = sqlite3.connect('morbilidade.db')
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute("""
    SELECT g.genero, SUM(e.obitos), SUM(e.ambulatorio), SUM(e.internamentos)
    FROM ESTATISTICAS e
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    GROUP BY g.genero
    """)
    results = cursor.fetchall()
    
    # Process results
    data = {"labels": ["Óbitos", "Ambulatório", "Internamentos"], "datasets": []}
    color_map = {}  # To store colors for each gender

    for row in results:
        genero, obitos, ambulatorio, internamentos = row
        
        # Assign a random color for each new gender
        if genero == "F":
            g = "Mulheres"
            background_color = 'rgba(255, 99, 132, 0.2)'
            border_color = 'rgb(255, 99, 132)'
            color_map[genero] = (background_color, border_color)
        elif genero == "M":
            g = "Homens"
            background_color = 'rgba(54, 162, 235, 0.2)'
            border_color = 'rgb(54, 162, 235)'
            color_map[genero] = (background_color, border_color)
        else:
            g = "Indefinido"
            background_color, border_color = get_random_color()
            color_map[genero] = (background_color, border_color)
        
        # Get colors from the map
        background_color, border_color = color_map[genero]
        
        dataset = {
            "label": g,
            "data": [ambulatorio, internamentos, obitos],
            "backgroundColor": background_color,
            "borderColor": border_color,
            "borderWidth": 1
        }
        data["datasets"].append(dataset)
    
    conn.close()
    return jsonify(data)

@APP.route('/radar-data-faixa')
def radar_data_faixa():
    # Connect to your database

    faixa_etaria = {
        1: "0-1",
        2: "1-5",
        3: "5-15",
        4: "15-25",
        5: "25-45",
        6: "45-65",
        7: "65-120"
    }

    conn = sqlite3.connect('morbilidade.db')
    cursor = conn.cursor()
    
    # Execute the query
    cursor.execute("""
    SELECT g.faixa_etaria_id, SUM(e.obitos), SUM(e.ambulatorio), SUM(e.internamentos)
    FROM ESTATISTICAS e
    JOIN GRUPOS g ON e.paciente_id = g.paciente_id
    GROUP BY g.faixa_etaria_id
    """)
    results = cursor.fetchall()
    
    # Process results
    data = {"labels": ["Óbitos", "Ambulatório", "Internamentos"], "datasets": []}
    color_map = {}  # To store colors for each gender

    for row in results:
        faixa, obitos, ambulatorio, internamentos = row
    
        if faixa not in color_map:
            background_color, border_color = get_random_color()
            color_map[faixa] = (background_color, border_color)
        
        # Get colors from the map
        background_color, border_color = color_map[faixa]
        
        dataset = {
            "label": faixa_etaria.get(faixa, "Invalid ID"),
            "data": [ambulatorio, internamentos, obitos],
            "backgroundColor": background_color,
            "borderColor": border_color,
            "borderWidth": 1
        }
        data["datasets"].append(dataset)
    
    conn.close()
    return jsonify(data)

@APP.route('/line-data')
def line_data():
    try:
        conn = sqlite3.connect('morbilidade.db')
        cursor = conn.cursor()
        
        # Query the data
        cursor.execute("""
        SELECT e.periodo, SUM(e.obitos), SUM(e.ambulatorio), SUM(e.internamentos)
        FROM ESTATISTICAS e
        GROUP BY e.periodo
        """)
        results = cursor.fetchall()

        # Process results
        data = {
            "labels": [],
            "datasets": [
                {"label": "Óbitos", "data": [], "backgroundColor": "rgba(255, 99, 132, 0.2)", "borderColor": "rgba(255, 99, 132, 1)", "fill": False},
                {"label": "Ambulatório", "data": [], "backgroundColor": "rgba(54, 162, 235, 0.2)", "borderColor": "rgba(54, 162, 235, 1)", "fill": False},
                {"label": "Internamentos", "data": [], "backgroundColor": "rgba(75, 192, 192, 0.2)", "borderColor": "rgba(75, 192, 192, 1)", "fill": False},
            ]
        }
        
        for row in results:
            periodo, obitos, ambulatorio, internamentos = row
            data["labels"].append(periodo)
            data["datasets"][0]["data"].append(obitos)
            data["datasets"][1]["data"].append(ambulatorio)
            data["datasets"][2]["data"].append(internamentos)
        
        conn.close()
        return jsonify(data)
    
    except sqlite3.OperationalError as e:
        return jsonify({"error": str(e), "message": "Please ensure the ESTATISTICAS table exists in the database."}), 500

SQL_FOLDER = os.path.join(os.path.dirname(__file__), 'sql')

def execute_query_from_file(file_number):
    """Read a SQL query from a file and execute it."""
    sql_file_path = os.path.join(SQL_FOLDER, f"{file_number}.sql")
    if not os.path.exists(sql_file_path):
        return {"error": f"SQL file {file_number}.sql not found."}

    try:
        with open(sql_file_path, 'r') as sql_file:
            query = sql_file.read()
        conn = sqlite3.connect('morbilidade.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return {"columns": columns, "results": results, "query": query}
    except sqlite3.Error as e:
        return {"error": str(e)}

@APP.route('/query-result/<int:file_number>', methods=['GET'])
def query_result(file_number):
    query_result = execute_query_from_file(file_number)
    return render_template('query_result.html', query_result=query_result, file_number=file_number)

@APP.route('/queries')
def query_form():
    """Display a list of available queries."""
    sql_files = [f for f in os.listdir(SQL_FOLDER) if f.endswith('.sql')]
    query_numbers = sorted(int(f.split('.')[0]) for f in sql_files)
    return render_template('queries.html', query_numbers=query_numbers)