from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from rdkit import Chem
from rdkit.Chem import AllChem
import json
import random
from datetime import datetime
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = 'organic_chemistry_secret_key_2024'  # For session management

# Configure Gemini API
# Note: Set your GEMINI_API_KEY environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
if GEMINI_API_KEY and GEMINI_API_KEY != 'your-api-key-here':
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to current model name
else:
    model = None

# CBSE Class 12 Organic Compounds Database
ORGANIC_COMPOUNDS = {
    # Alcohols
    "methanol": {
        "name": "Methanol",
        "formula": "CH₃OH",
        "smiles": "CO",
        "category": "Alcohols",
        "description": "Primary alcohol, simplest alcohol",
        "preparation": {
            "method": "Industrial synthesis from syngas",
            "equation": "CO + 2H₂ → CH₃OH",
            "reagents": ["Carbon monoxide", "Hydrogen gas"],
            "conditions": "High pressure (50-100 atm), 250°C, Cu/ZnO catalyst"
        }
    },
    "ethanol": {
        "name": "Ethanol",
        "formula": "C₂H₅OH",
        "smiles": "CCO",
        "category": "Alcohols",
        "description": "Primary alcohol, drinking alcohol",
        "preparation": {
            "method": "Fermentation or hydration of ethene",
            "equation": "C₂H₄ + H₂O → C₂H₅OH",
            "reagents": ["Ethene", "Water"],
            "conditions": "H₃PO₄ catalyst, 300°C, high pressure"
        }
    },
    "propanol": {
        "name": "1-Propanol",
        "formula": "C₃H₇OH",
        "smiles": "CCCO",
        "category": "Alcohols",
        "description": "Primary alcohol"
    },
    "isopropanol": {
        "name": "2-Propanol (Isopropanol)",
        "formula": "C₃H₇OH",
        "smiles": "CC(C)O",
        "category": "Alcohols",
        "description": "Secondary alcohol, rubbing alcohol"
    },
    "butanol": {
        "name": "1-Butanol",
        "formula": "C₄H₉OH",
        "smiles": "CCCCO",
        "category": "Alcohols",
        "description": "Primary alcohol"
    },
    "phenol": {
        "name": "Phenol",
        "formula": "C₆H₅OH",
        "smiles": "c1ccc(cc1)O",
        "category": "Alcohols",
        "description": "Aromatic alcohol, carbolic acid"
    },
    
    # Aldehydes
    "formaldehyde": {
        "name": "Formaldehyde",
        "formula": "HCHO",
        "smiles": "C=O",
        "category": "Aldehydes",
        "description": "Simplest aldehyde, used in preservation"
    },
    "acetaldehyde": {
        "name": "Acetaldehyde",
        "formula": "CH₃CHO",
        "smiles": "CC=O",
        "category": "Aldehydes",
        "description": "Ethanal, produced in alcohol metabolism",
        "preparation": {
            "method": "Oxidation of ethanol",
            "equation": "C₂H₅OH + [O] → CH₃CHO + H₂O",
            "reagents": ["Ethanol", "Oxidizing agent (K₂Cr₂O₇/H₂SO₄)"],
            "conditions": "Controlled oxidation, distillation"
        }
    },
    "benzaldehyde": {
        "name": "Benzaldehyde",
        "formula": "C₆H₅CHO",
        "smiles": "c1ccc(cc1)C=O",
        "category": "Aldehydes",
        "description": "Aromatic aldehyde, almond flavor"
    },
    
    # Ketones
    "acetone": {
        "name": "Acetone",
        "formula": "CH₃COCH₃",
        "smiles": "CC(=O)C",
        "category": "Ketones",
        "description": "Simplest ketone, nail polish remover",
        "preparation": {
            "method": "Oxidation of 2-propanol",
            "equation": "(CH₃)₂CHOH + [O] → (CH₃)₂CO + H₂O",
            "reagents": ["2-Propanol", "Oxidizing agent (K₂Cr₂O₇/H₂SO₄)"],
            "conditions": "Reflux with oxidizing agent"
        }
    },
    "butanone": {
        "name": "Butanone (MEK)",
        "formula": "C₄H₈O",
        "smiles": "CCC(=O)C",
        "category": "Ketones",
        "description": "Methyl ethyl ketone, industrial solvent"
    },
    
    # Carboxylic Acids
    "formic_acid": {
        "name": "Formic Acid",
        "formula": "HCOOH",
        "smiles": "C(=O)O",
        "category": "Carboxylic Acids",
        "description": "Methanoic acid, found in ant stings"
    },
    "acetic_acid": {
        "name": "Acetic Acid",
        "formula": "CH₃COOH",
        "smiles": "CC(=O)O",
        "category": "Carboxylic Acids",
        "description": "Ethanoic acid, vinegar",
        "preparation": {
            "method": "Oxidation of acetaldehyde",
            "equation": "CH₃CHO + [O] → CH₃COOH",
            "reagents": ["Acetaldehyde", "Oxidizing agent (KMnO₄)"],
            "conditions": "Alkaline KMnO₄, followed by acidification"
        }
    },
    "benzoic_acid": {
        "name": "Benzoic Acid",
        "formula": "C₆H₅COOH",
        "smiles": "c1ccc(cc1)C(=O)O",
        "category": "Carboxylic Acids",
        "description": "Aromatic carboxylic acid, food preservative"
    },
    
    # Esters
    "methyl_acetate": {
        "name": "Methyl Acetate",
        "formula": "CH₃COOCH₃",
        "smiles": "CC(=O)OC",
        "category": "Esters",
        "description": "Ester of acetic acid and methanol"
    },
    "ethyl_acetate": {
        "name": "Ethyl Acetate",
        "formula": "CH₃COOC₂H₅",
        "smiles": "CC(=O)OCC",
        "category": "Esters",
        "description": "Ester of acetic acid and ethanol, nail polish remover",
        "preparation": {
            "method": "Esterification reaction",
            "equation": "CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O",
            "reagents": ["Acetic acid", "Ethanol", "Conc. H₂SO₄"],
            "conditions": "Reflux with conc. H₂SO₄ as catalyst"
        }
    },
    
    # Amines
    "methylamine": {
        "name": "Methylamine",
        "formula": "CH₃NH₂",
        "smiles": "CN",
        "category": "Amines",
        "description": "Primary amine"
    },
    "dimethylamine": {
        "name": "Dimethylamine",
        "formula": "(CH₃)₂NH",
        "smiles": "CNC",
        "category": "Amines",
        "description": "Secondary amine"
    },
    "aniline": {
        "name": "Aniline",
        "formula": "C₆H₅NH₂",
        "smiles": "c1ccc(cc1)N",
        "category": "Amines",
        "description": "Aromatic amine, used in dye production"
    },
    
    # Hydrocarbons
    "methane": {
        "name": "Methane",
        "formula": "CH₄",
        "smiles": "C",
        "category": "Alkanes",
        "description": "Simplest alkane, natural gas"
    },
    "ethane": {
        "name": "Ethane",
        "formula": "C₂H₆",
        "smiles": "CC",
        "category": "Alkanes",
        "description": "Two-carbon alkane"
    },
    "propane": {
        "name": "Propane",
        "formula": "C₃H₈",
        "smiles": "CCC",
        "category": "Alkanes",
        "description": "Three-carbon alkane, LPG"
    },
    "butane": {
        "name": "Butane",
        "formula": "C₄H₁₀",
        "smiles": "CCCC",
        "category": "Alkanes",
        "description": "Four-carbon alkane, lighter fuel"
    },
    "ethene": {
        "name": "Ethene (Ethylene)",
        "formula": "C₂H₄",
        "smiles": "C=C",
        "category": "Alkenes",
        "description": "Simplest alkene, plant hormone"
    },
    "propene": {
        "name": "Propene",
        "formula": "C₃H₆",
        "smiles": "CC=C",
        "category": "Alkenes",
        "description": "Three-carbon alkene"
    },
    "ethyne": {
        "name": "Ethyne (Acetylene)",
        "formula": "C₂H₂",
        "smiles": "C#C",
        "category": "Alkynes",
        "description": "Simplest alkyne, welding gas"
    },
    "benzene": {
        "name": "Benzene",
        "formula": "C₆H₆",
        "smiles": "c1ccccc1",
        "category": "Aromatic",
        "description": "Simplest aromatic compound"
    },
    "toluene": {
        "name": "Toluene",
        "formula": "C₇H₈",
        "smiles": "Cc1ccccc1",
        "category": "Aromatic",
        "description": "Methylbenzene, solvent"
    },
    "naphthalene": {
        "name": "Naphthalene",
        "formula": "C₁₀H₈",
        "smiles": "c1ccc2ccccc2c1",
        "category": "Aromatic",
        "description": "Bicyclic aromatic compound, mothballs"
    },
    
    # Ethers
    "diethyl_ether": {
        "name": "Diethyl Ether",
        "formula": "C₂H₅OC₂H₅",
        "smiles": "CCOCC",
        "category": "Ethers",
        "description": "Common ether, anesthetic"
    },
    
    # Haloalkanes
    "chloromethane": {
        "name": "Chloromethane",
        "formula": "CH₃Cl",
        "smiles": "CCl",
        "category": "Haloalkanes",
        "description": "Methyl chloride"
    },
    "chloroform": {
        "name": "Chloroform",
        "formula": "CHCl₃",
        "smiles": "C(Cl)(Cl)Cl",
        "category": "Haloalkanes",
        "description": "Trichloromethane, former anesthetic"
    }
}

# Quiz Database
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the molecular formula of ethanol?",
        "options": ["C₂H₆O", "C₂H₄O", "C₃H₈O", "CH₄O"],
        "correct": 0,
        "explanation": "Ethanol has 2 carbon atoms, 6 hydrogen atoms, and 1 oxygen atom: C₂H₆O"
    },
    {
        "id": 2,
        "question": "Which reagent is used to convert ethanol to acetaldehyde?",
        "options": ["NaOH", "K₂Cr₂O₇/H₂SO₄", "NH₃", "HCl"],
        "correct": 1,
        "explanation": "K₂Cr₂O₇/H₂SO₄ is a controlled oxidizing agent that converts primary alcohols to aldehydes"
    },
    {
        "id": 3,
        "question": "What type of reaction forms ethyl acetate from acetic acid and ethanol?",
        "options": ["Addition", "Substitution", "Esterification", "Elimination"],
        "correct": 2,
        "explanation": "Esterification is the reaction between a carboxylic acid and alcohol to form an ester"
    },
    {
        "id": 4,
        "question": "Which compound is known as wood spirit?",
        "options": ["Ethanol", "Methanol", "Propanol", "Butanol"],
        "correct": 1,
        "explanation": "Methanol is called wood spirit because it was originally produced by destructive distillation of wood"
    },
    {
        "id": 5,
        "question": "What is the IUPAC name of acetone?",
        "options": ["Propanone", "Butanone", "Ethanone", "Pentanone"],
        "correct": 0,
        "explanation": "Acetone is a 3-carbon ketone, so its IUPAC name is propanone"
    },
    {
        "id": 6,
        "question": "Which functional group is present in aldehydes?",
        "options": ["-OH", "-CHO", "-COOH", "-NH₂"],
        "correct": 1,
        "explanation": "Aldehydes contain the -CHO (carbonyl) functional group"
    },
    {
        "id": 7,
        "question": "What catalyst is used in the industrial preparation of methanol?",
        "options": ["Ni", "Pt", "Cu/ZnO", "Fe"],
        "correct": 2,
        "explanation": "Cu/ZnO catalyst is used in the industrial synthesis of methanol from syngas"
    },
    {
        "id": 8,
        "question": "Which compound is formed by the oxidation of 2-propanol?",
        "options": ["Propanal", "Propanoic acid", "Propanone", "Propene"],
        "correct": 2,
        "explanation": "Secondary alcohols are oxidized to ketones. 2-propanol oxidizes to propanone (acetone)"
    },
    {
        "id": 9,
        "question": "What is the common name of ethanoic acid?",
        "options": ["Formic acid", "Acetic acid", "Propionic acid", "Butyric acid"],
        "correct": 1,
        "explanation": "Ethanoic acid is commonly known as acetic acid, the main component of vinegar"
    },
    {
        "id": 10,
        "question": "Which compound has the molecular formula C₆H₆?",
        "options": ["Cyclohexane", "Benzene", "Toluene", "Phenol"],
        "correct": 1,
        "explanation": "Benzene is the simplest aromatic compound with molecular formula C₆H₆"
    },
    {
        "id": 11,
        "question": "What type of amine is aniline?",
        "options": ["Primary", "Secondary", "Tertiary", "Quaternary"],
        "correct": 0,
        "explanation": "Aniline (C₆H₅NH₂) has one alkyl/aryl group attached to nitrogen, making it a primary amine"
    },
    {
        "id": 12,
        "question": "Which reaction converts alkenes to alcohols?",
        "options": ["Hydration", "Dehydration", "Oxidation", "Reduction"],
        "correct": 0,
        "explanation": "Hydration reaction adds water across the double bond of alkenes to form alcohols"
    },
    {
        "id": 13,
        "question": "What is the product when ethanol is heated with conc. H₂SO₄ at 170°C?",
        "options": ["Ethene", "Acetaldehyde", "Acetic acid", "Diethyl ether"],
        "correct": 0,
        "explanation": "At 170°C, ethanol undergoes dehydration to form ethene (elimination reaction)"
    },
    {
        "id": 14,
        "question": "Which compound is used as a preservative and antiseptic?",
        "options": ["Methanol", "Ethanol", "Phenol", "Acetone"],
        "correct": 2,
        "explanation": "Phenol has antiseptic properties and was historically used as a disinfectant"
    },
    {
        "id": 15,
        "question": "What is the hybridization of carbon in benzene?",
        "options": ["sp³", "sp²", "sp", "sp³d"],
        "correct": 1,
        "explanation": "All carbon atoms in benzene are sp² hybridized, forming a planar hexagonal structure"
    }
]

def generate_3d_coordinates(smiles):
    """Generate 3D coordinates for a molecule from SMILES"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        
        conf = mol.GetConformer()
        atoms = []
        bonds = []
        
        # Get atom information
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            atoms.append({
                'element': atom.GetSymbol(),
                'x': pos.x,
                'y': pos.y,
                'z': pos.z,
                'id': atom.GetIdx()
            })
        
        # Get bond information
        for bond in mol.GetBonds():
            bonds.append({
                'atom1': bond.GetBeginAtomIdx(),
                'atom2': bond.GetEndAtomIdx(),
                'order': bond.GetBondType().name
            })
        
        return {'atoms': atoms, 'bonds': bonds}
    except Exception as e:
        print(f"Error generating 3D coordinates: {e}")
        return None

@app.route('/')
def index():
    """Main page showing all compounds"""
    categories = {}
    for compound_id, compound in ORGANIC_COMPOUNDS.items():
        category = compound['category']
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'id': compound_id,
            'name': compound['name'],
            'formula': compound['formula'],
            'description': compound['description']
        })
    
    return render_template('index.html', categories=categories)

@app.route('/compound/<compound_id>')
def compound_detail(compound_id):
    """Show detailed view of a specific compound"""
    if compound_id not in ORGANIC_COMPOUNDS:
        return "Compound not found", 404
    
    compound = ORGANIC_COMPOUNDS[compound_id]
    return render_template('compound.html', compound=compound, compound_id=compound_id)

@app.route('/api/compound/<compound_id>/3d')
def get_3d_structure(compound_id):
    """API endpoint to get 3D structure data"""
    if compound_id not in ORGANIC_COMPOUNDS:
        return jsonify({'error': 'Compound not found'}), 404
    
    compound = ORGANIC_COMPOUNDS[compound_id]
    structure_data = generate_3d_coordinates(compound['smiles'])
    
    if structure_data is None:
        return jsonify({'error': 'Could not generate 3D structure'}), 500
    
    return jsonify({
        'compound': compound,
        'structure': structure_data
    })

@app.route('/quiz')
def quiz_home():
    """Quiz home page"""
    return render_template('quiz.html')

@app.route('/quiz/start')
def start_quiz():
    """Start a new quiz session"""
    # Select random questions for the quiz
    selected_questions = random.sample(QUIZ_QUESTIONS, min(10, len(QUIZ_QUESTIONS)))
    
    # Store quiz data in session
    session['quiz_questions'] = selected_questions
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    session['start_time'] = datetime.now().isoformat()
    
    return render_template('quiz_question.html', 
                         question=selected_questions[0], 
                         question_num=1, 
                         total_questions=len(selected_questions))

@app.route('/quiz/question/<int:question_num>')
def quiz_question(question_num):
    """Display a specific quiz question"""
    if 'quiz_questions' not in session:
        return redirect(url_for('quiz_home'))
    
    questions = session['quiz_questions']
    if question_num < 1 or question_num > len(questions):
        return redirect(url_for('quiz_results'))
    
    question = questions[question_num - 1]
    return render_template('quiz_question.html', 
                         question=question, 
                         question_num=question_num, 
                         total_questions=len(questions))

@app.route('/quiz/submit', methods=['POST'])
def submit_answer():
    """Submit an answer and move to next question"""
    if 'quiz_questions' not in session:
        return redirect(url_for('quiz_home'))
    
    questions = session['quiz_questions']
    current_q = session['current_question']
    
    if current_q >= len(questions):
        return redirect(url_for('quiz_results'))
    
    # Get submitted answer
    selected_answer = request.form.get('answer')
    if selected_answer is not None:
        selected_answer = int(selected_answer)
        
        # Check if answer is correct
        correct_answer = questions[current_q]['correct']
        is_correct = selected_answer == correct_answer
        
        # Store answer
        session['answers'].append({
            'question_id': questions[current_q]['id'],
            'selected': selected_answer,
            'correct': correct_answer,
            'is_correct': is_correct
        })
        
        # Update score
        if is_correct:
            session['score'] += 1
        
        # Move to next question
        session['current_question'] += 1
        
        # Check if quiz is complete
        if session['current_question'] >= len(questions):
            return redirect(url_for('quiz_results'))
        else:
            return redirect(url_for('quiz_question', question_num=session['current_question'] + 1))
    
    # If no answer selected, stay on current question
    return redirect(url_for('quiz_question', question_num=current_q + 1))

@app.route('/quiz/results')
def quiz_results():
    """Display quiz results"""
    if 'quiz_questions' not in session or 'score' not in session:
        return redirect(url_for('quiz_home'))
    
    questions = session['quiz_questions']
    answers = session['answers']
    score = session['score']
    total_questions = len(questions)
    
    # Calculate percentage
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Determine grade
    if percentage >= 90:
        grade = 'A+'
        message = 'Excellent! Outstanding knowledge of organic chemistry!'
    elif percentage >= 80:
        grade = 'A'
        message = 'Great job! You have a strong understanding of the concepts.'
    elif percentage >= 70:
        grade = 'B'
        message = 'Good work! Keep studying to improve further.'
    elif percentage >= 60:
        grade = 'C'
        message = 'Fair performance. Review the concepts and try again.'
    else:
        grade = 'F'
        message = 'Keep studying well! Practice more with the 3D models to understand better.'
    
    # Calculate time taken
    start_time = datetime.fromisoformat(session['start_time'])
    end_time = datetime.now()
    time_taken = end_time - start_time
    
    # Prepare detailed results
    detailed_results = []
    for i, answer in enumerate(answers):
        question = questions[i]
        detailed_results.append({
            'question': question['question'],
            'options': question['options'],
            'selected': answer['selected'],
            'correct': answer['correct'],
            'is_correct': answer['is_correct'],
            'explanation': question['explanation']
        })
    
    return render_template('quiz_results.html',
                         score=score,
                         total_questions=total_questions,
                         percentage=round(percentage, 1),
                         grade=grade,
                         message=message,
                         time_taken=str(time_taken).split('.')[0],  # Remove microseconds
                         detailed_results=detailed_results)

@app.route('/quiz/reset')
def reset_quiz():
    """Reset quiz session"""
    session.pop('quiz_questions', None)
    session.pop('current_question', None)
    session.pop('score', None)
    session.pop('answers', None)
    session.pop('start_time', None)
    return redirect(url_for('quiz_home'))

@app.route('/query')
def query_page():
    """Display the query page with text input"""
    return render_template('query.html')

@app.route('/query/ask', methods=['POST'])
def ask_gemini():
    """Handle Gemini API queries"""
    user_question = request.form.get('question', '').strip()
    
    if not user_question:
        return jsonify({'error': 'Please enter a question'}), 400
    
    if not model:
        return jsonify({
            'error': 'Gemini API is not configured. Please set the GEMINI_API_KEY environment variable.'
        }), 500
    
    try:
        # Create a context-aware prompt for organic chemistry
        context_prompt = f"""You are an expert organic chemistry tutor for CBSE Class 12 students. 
        Please provide a clear, educational answer to the following question about organic chemistry.
        Focus on CBSE Class 12 syllabus topics including: alcohols, aldehydes, ketones, carboxylic acids, 
        esters, amines, hydrocarbons, and their reactions, preparations, and properties.
        
        Question: {user_question}
        
        Please provide a comprehensive but student-friendly answer."""
        
        response = model.generate_content(context_prompt)
        
        # Check if response has text
        if not response.text:
            return jsonify({
                'error': 'No response generated. Please try rephrasing your question.'
            }), 500
        
        return jsonify({
            'question': user_question,
            'answer': response.text,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        error_message = str(e)
        
        # Provide more helpful error messages for common issues
        if '404' in error_message and 'model' in error_message.lower():
            error_message = 'Model not available. Please check if your API key has access to Gemini models.'
        elif 'quota' in error_message.lower():
            error_message = 'API quota exceeded. Please check your Gemini API usage limits.'
        elif 'authentication' in error_message.lower() or 'api key' in error_message.lower():
            error_message = 'Invalid API key. Please check your GEMINI_API_KEY environment variable.'
        
        return jsonify({
            'error': f'Error generating response: {error_message}'
        }), 500

if __name__ == '__main__':
    import signal
    import sys
    
    def signal_handler(sig, frame):
        print('\n🛑 Shutting down Flask application gracefully...')
        sys.exit(0)
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    try:
        print('🚀 Starting Flask application on http://localhost:6061')
        print('📚 Access your Organic Chemistry 3D app!')
        print('🧪 Quiz available at: http://localhost:6061/quiz')
        print('⚠️  Press Ctrl+C to stop the server')
        
        app.run(
            debug=False,  # Set to False for production
            host='0.0.0.0', 
            port=8090,  # Alternative port 
            use_reloader=False,  # Disable reloader for production
            threaded=True
        )
    except KeyboardInterrupt:
        print('\n🛑 Server stopped by user')
    except Exception as e:
        print(f'\n❌ Server error: {e}')
    finally:
        print('✅ Flask application shutdown complete')
