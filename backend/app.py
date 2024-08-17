from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import csv
import os
import logging
from classifier import get_next_question, get_next_tier, TIERS, QUESTIONS

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Set the CSV_FILE path relative to the current directory
CSV_FILE = os.path.join(current_dir, 'skill_tierlist.csv')

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../frontend')
CORS(app)

def detect_delimiter(file_path):
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()
        if '|' in first_line:
            return '|'
        elif ',' in first_line:
            return ','
        else:
            raise ValueError("Unable to detect CSV delimiter. Please use '|' or ',' as delimiter.")

def read_csv():
    try:
        delimiter = detect_delimiter(CSV_FILE)
        with open(CSV_FILE, 'r') as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no headers")
            if 'skill' not in reader.fieldnames:
                raise ValueError(f"CSV file is missing the 'skill' column. Found columns: {', '.join(reader.fieldnames)}")
            data = list(reader)
            if not data:
                raise ValueError("CSV file has no data rows")
            return [{'tier': row.get('tier', ''), 'skill': row['skill']} for row in data]
    except FileNotFoundError:
        logger.error(f"CSV file not found: {CSV_FILE}")
        raise
    except csv.Error as e:
        logger.error(f"CSV parsing error: {str(e)}")
        raise
    except ValueError as e:
        logger.error(str(e))
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading CSV file: {str(e)}")
        raise

def write_csv(data):
    try:
        delimiter = detect_delimiter(CSV_FILE)
        fieldnames = ['tier', 'skill']
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        logger.error(f"Error writing to CSV file: {str(e)}")
        raise

def validate_csv():
    try:
        read_csv()
        logger.info("CSV file validated successfully")
    except Exception as e:
        logger.error(f"CSV file validation failed: {str(e)}")
        raise

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/next-skill', methods=['GET'])
def next_skill():
    try:
        skills = read_csv()
        for skill in skills:
            if not skill.get('tier'):
                return jsonify({'skill': skill['skill'], 'question': get_next_question('E'), 'tier': 'E', 'questionIndex': 0})
        return jsonify({'message': 'All skills classified'})
    except Exception as e:
        logger.error(f"Error in next_skill: {str(e)}")
        return jsonify(error=f"An error occurred while fetching the next skill: {str(e)}"), 500

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    try:
        data = request.json
        skill = data['skill']
        answer = data['answer']
        current_tier = data['currentTier']
        question_index = int(data.get('questionIndex', 0))

        logger.info(f"Received data: {data}")
        logger.info(f"Processing answer for skill: {skill}, tier: {current_tier}, question index: {question_index}, answer: {answer}")

        skills = read_csv()
        skill_found = False
        for s in skills:
            if s['skill'] == skill:
                skill_found = True
                if answer == 'no':
                    s['tier'] = current_tier
                    write_csv(skills)
                    logger.info(f"Skill {skill} classified as tier {current_tier}")
                    return jsonify({'message': 'Skill classified', 'tier': current_tier})
                else:
                    try:
                        if question_index + 1 < len(QUESTIONS[current_tier]):
                            next_question = get_next_question(current_tier, question_index + 1)
                            logger.info(f"Moving to next question for skill {skill}, tier {current_tier}, question index {question_index + 1}")
                            return jsonify({'question': next_question, 'tier': current_tier, 'questionIndex': question_index + 1})
                        else:
                            next_tier = get_next_tier(current_tier)
                            if next_tier:
                                logger.info(f"Moving to next tier for skill {skill}, new tier {next_tier}")
                                return jsonify({'question': get_next_question(next_tier), 'tier': next_tier, 'questionIndex': 0})
                            else:
                                s['tier'] = current_tier
                                write_csv(skills)
                                logger.info(f"Skill {skill} classified as highest tier {current_tier}")
                                return jsonify({'message': 'Skill classified', 'tier': current_tier})
                    except KeyError:
                        logger.error(f"KeyError: Tier {current_tier} not found in QUESTIONS dictionary")
                        return jsonify({'error': f"Invalid tier: {current_tier}"}), 400
                break

        if not skill_found:
            logger.warning(f"Skill {skill} not found in CSV")
            return jsonify({'error': 'Skill not found'}), 404

        write_csv(skills)
        return jsonify({'message': 'Answer submitted successfully'})
    except Exception as e:
        logger.error(f"Error in submit_answer: {str(e)}. Received data: {request.json}")
        return jsonify({'error': f"An error occurred while submitting the answer: {str(e)}"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"An unhandled error occurred: {str(e)}")
    return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

if __name__ == '__main__':
    try:
        validate_csv()
        app.run(debug=True, port=2139)
    except Exception as e:
        logger.error(f"Failed to start the application: {str(e)}")