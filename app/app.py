import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = {}
    stats = db.execute('''
    SELECT * FROM
      (SELECT COUNT(*) s_doenca FROM doenca)
    JOIN
      (SELECT COUNT(*) s_estatistica FROM estatistica)
    JOIN
      (SELECT COUNT(*) s_faixa FROM faixa_etaria)
    JOIN 
      (SELECT COUNT(*) s_hospital FROM hospital)
    JOIN 
      (SELECT COUNT(*) s_paciente FROM paciente)
    JOIN 
      (SELECT COUNT(*) s_regiao FROM regiao)
    ''').fetchone()
    logging.info(stats)
    return render_template('index.html',stats=stats)

# ---------------------------------- HOSPITAIS --------------------------------------------

@APP.route('/hospitals/')
def list_hospitais():
    hospitals = db.execute(
      '''
      SELECT *
      FROM hospital
      ORDER BY hospital_id
      ''').fetchall()
    return render_template('hospital-list.html', hospitals=hospitals)

@APP.route('/hospitals/<int:id>/')
def get_hospital(id):
  hospital = db.execute(
      '''
      SELECT *
      FROM hospital 
      WHERE hospital_id = ?
      ''', [id]).fetchone()

  if hospital is None:
     abort(404, 'Hospital id {} does not exist.'.format(id))

  region = db.execute(
      '''
      SELECT r.nome
      FROM hospital h
      JOIN regiao r ON h.regiao_id = r.regiao_id
      WHERE hospital_id = ?
      ''', [id]).fetchone()

  diseases = db.execute(
    '''
    SELECT DISTINCT h.nome, d.doenca_id, d.descricao
    FROM hospital h
    JOIN estatistica e ON e.hospital_id = h.hospital_id
    JOIN doenca d ON d.doenca_id = e.doenca_id
    WHERE h.hospital_id = ?
    ORDER BY d.doenca_id
    ''', [id]).fetchall()
  
  return render_template('hospital.html', hospital=hospital, region=region, diseases=diseases)

@APP.route('/hospitals/<int:id_h>/<int:id_d>/')
def get_hospital_disease(id_h, id_d):
  stats = db.execute(
      '''
      SELECT DISTINCT d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, count(obitos) as o, count(ambulatorio) as a, count(internamentos) as i
      FROM doenca d
      JOIN estatistica e ON d.doenca_id = e.doenca_id
      JOIN hospital h on h.hospital_id = e.hospital_id
      JOIN regiao r on r.regiao_id = h.regiao_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      ''', [id_d, id_h]).fetchone()

  if stats is None:
     abort(404, 'Stats id {} does not exist.'.format(id))

  genero = db.execute(
      '''
      SELECT p.genero, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, count(obitos) as o, count(ambulatorio) as a, count(internamentos) as i
      FROM doenca d
      JOIN estatistica e ON d.doenca_id = e.doenca_id
      JOIN hospital h ON h.hospital_id = e.hospital_id
      JOIN regiao r ON r.regiao_id = h.regiao_id
      JOIN paciente p ON p.paciente_id = e.paciente_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      GROUP BY p.genero
      ''', [id_d, id_h]).fetchall()

  faixa = db.execute(
      '''
      SELECT CONCAT(idade_min, '-', idade_max) AS age_range, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, count(obitos) as o, count(ambulatorio) as a, count(internamentos) as i
      FROM doenca d
      JOIN estatistica e ON d.doenca_id = e.doenca_id
      JOIN hospital h ON h.hospital_id = e.hospital_id
      JOIN regiao r ON r.regiao_id = h.regiao_id
      JOIN paciente p ON p.paciente_id = e.paciente_id
      JOIN faixa_etaria f ON p.faixa_etaria_id = f.faixa_etaria_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      GROUP BY p.faixa_etaria_id
      ''', [id_d, id_h]).fetchall()

  ambos = db.execute(
      '''
      SELECT CONCAT(idade_min, '-', idade_max) AS age_range, p.genero, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, count(obitos) as o, count(ambulatorio) as a, count(internamentos) as i
      FROM doenca d
      JOIN estatistica e ON d.doenca_id = e.doenca_id
      JOIN hospital h ON h.hospital_id = e.hospital_id
      JOIN regiao r ON r.regiao_id = h.regiao_id
      JOIN paciente p ON p.paciente_id = e.paciente_id
      JOIN faixa_etaria f ON p.faixa_etaria_id = f.faixa_etaria_id
      WHERE d.doenca_id = ? AND h.hospital_id = ?
      GROUP BY p.faixa_etaria_id, p.genero
      ORDER BY p.genero
      ''', [id_d, id_h]).fetchall()

  periodo = db.execute(
      '''
      SELECT e.periodo, d.doenca_id, d.descricao, r.regiao_id, r.nome as regiao, h.hospital_id, h.nome as hospital, count(obitos) as o, count(ambulatorio) as a, count(internamentos) as i
      FROM doenca d
      JOIN estatistica e ON d.doenca_id = e.doenca_id
      JOIN hospital h ON h.hospital_id = e.hospital_id
      JOIN regiao r ON r.regiao_id = h.regiao_id
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
      FROM regiao
      ORDER BY regiao_id
      ''').fetchall()
    return render_template('region-list.html', regions=regions)


# ------------------------------------------------- DOENCAS

@APP.route('/diseases/')
def list_diseases():
    diseases = db.execute(
      '''
      SELECT *
      FROM doenca
      ORDER BY doenca_id
      ''').fetchall()
    return render_template('doenca-list.html', diseases=diseases)

@APP.route('/diseases/<int:id>/')
def get_disease(id):
    count = db.execute(
      '''
      SELECT count(obitos) AS o, count(ambulatorio) AS a, count(internamentos) AS i, d.doenca_id, d.descricao
      FROM doenca d
      NATURAL JOIN estatistica
      WHERE d.doenca_id = ?
      ''', [id]).fetchone()
    
    regions = db.execute(
      '''
      SELECT r.regiao_id, r.nome
      FROM doenca
      NATURAL JOIN estatistica
      NATURAL JOIN regiao r
      WHERE doenca_id = ?
      GROUP BY nome
      ORDER BY r.regiao_id
      ''', [id]).fetchall()

    hospitals = db.execute(
      '''
      SELECT h.hospital_id, h.nome
      FROM doenca
      NATURAL JOIN estatistica
      NATURAL JOIN hospital h
      WHERE doenca_id = ?
      GROUP BY nome
      ORDER BY h.hospital_id
      ''', [id]).fetchall()
    
    return render_template('doenca.html', count=count, regions=regions, hospitals=hospitals)