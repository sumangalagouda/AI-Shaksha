from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
from threading import Lock
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'reports.json')

os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'data', 'bundles'), exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

MEDIATIONS_FILE = os.path.join(BASE_DIR, 'data', 'mediations.json')
if not os.path.exists(MEDIATIONS_FILE):
    with open(MEDIATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

MEDIATORS_FILE = os.path.join(BASE_DIR, 'data', 'mediators.json')
if not os.path.exists(MEDIATORS_FILE):
    # seed with sample mediators (NGOs / lawyers)
    sample = [
        {"id": "ng01", "name": "Citizens Watch (NGO)", "contact": "ngo@citizens.example"},
        {"id": "law01", "name": "Public Interest Law Center", "contact": "law@pil.example"}
    ]
    with open(MEDIATORS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)

lock = Lock()

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, '..'))
CORS(app)


def read_reports():
    with lock:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)


def read_mediations():
    with lock:
        with open(MEDIATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)


def write_mediations(data):
    with lock:
        with open(MEDIATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def read_mediators():
    with lock:
        with open(MEDIATORS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)


def write_reports(data):
    with lock:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def parse_amount(a):
    if not a: return 0
    s = ''.join(ch for ch in str(a) if ch.isdigit())
    try:
        return int(s) if s else 0
    except Exception:
        return 0


@app.route('/api/report', methods=['POST'])
def add_report():
    payload = request.get_json(force=True)
    if not payload:
        return jsonify({'error': 'Invalid JSON'}), 400

    report = {
        'id': int(datetime.utcnow().timestamp()*1000),
        'date': payload.get('date') or datetime.utcnow().isoformat(),
        'department': payload.get('department'),
        'official': payload.get('official_name'),
        'bribe_amount': payload.get('bribe_amount'),
        'bribe_amount_value': parse_amount(payload.get('bribe_amount')),
        'location': payload.get('location'),
        'violation': payload.get('violation'),
        'authority': payload.get('authority_to_report'),
        'risk_level': payload.get('risk_level'),
        'evidence_strength': payload.get('evidence_strength'),
        'transcript': payload.get('transcript'),
        'anonymous': bool(payload.get('anonymous', True)),
        'created_at': datetime.utcnow().isoformat()
    }

    reports = read_reports()
    reports.insert(0, report)
    write_reports(reports)
    return jsonify({'ok': True, 'id': report['id']})


@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = read_reports()
    return jsonify(reports)


@app.route('/api/summary', methods=['GET'])
def summary():
    reports = read_reports()
    total = len(reports)
    complaints = sum(1 for r in reports if r.get('authority'))
    avg_amount = 0
    if total:
        avg_amount = sum(r.get('bribe_amount_value', 0) for r in reports) // total

    dept_counts = {}
    for r in reports:
        d = r.get('department') or 'Unknown'
        dept_counts[d] = dept_counts.get(d, 0) + 1

    top_departments = sorted(dept_counts.items(), key=lambda x: x[1], reverse=True)[:6]

    return jsonify({
        'total_reports': total,
        'complaints_filed': complaints,
        'avg_bribe_amount': avg_amount,
        'top_departments': top_departments
    })


@app.route('/api/mediators', methods=['GET'])
def mediators():
    return jsonify(read_mediators())


@app.route('/api/mediate', methods=['POST'])
def mediate():
    payload = request.get_json(force=True)
    if not payload:
        return jsonify({'error': 'Invalid JSON'}), 400

    # Create mediation record
    mid = int(datetime.utcnow().timestamp() * 1000)
    med = {
        'id': mid,
        'report_id': payload.get('report_id'),
        'report': payload.get('report'),
        'mediator_id': payload.get('mediator_id'),
        'mediator_contact': payload.get('mediator_contact'),
        'created_at': datetime.utcnow().isoformat()
    }

    med_list = read_mediations()
    med_list.insert(0, med)
    write_mediations(med_list)

    # Create anonymized bundle (text file with complaint + transcript)
    bundle_name = f"bundle_{mid}.txt"
    bundle_path = os.path.join(BASE_DIR, 'data', 'bundles', bundle_name)
    try:
        with open(bundle_path, 'w', encoding='utf-8') as bf:
            bf.write('--- ANONYMIZED BUNDLE ---\n')
            bf.write(f"Created: {med['created_at']}\n")
            bf.write('\n-- Complaint --\n')
            bf.write(payload.get('report', {}).get('complaint', '') + '\n')
            bf.write('\n-- Transcript (metadata removed) --\n')
            bf.write(payload.get('report', {}).get('transcript', '') + '\n')
    except Exception as e:
        return jsonify({'error': 'Failed to create bundle', 'details': str(e)}), 500

    # Return mediation info with bundle URL
    return jsonify({
        'ok': True,
        'mediation_id': mid,
        'bundle': f"/data/bundles/{bundle_name}",
        'mediator_contact': med['mediator_contact']
    })


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def static_proxy(path):
    # Serve files from project root (parent of backend)
    root = os.path.abspath(os.path.join(BASE_DIR, '..'))
    if os.path.exists(os.path.join(root, path)):
        return send_from_directory(root, path)
    return send_from_directory(root, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
