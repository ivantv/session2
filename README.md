# CBSE Class 12 Organic Chemistry 3D Visualizer

An interactive Flask web application that displays 3D animated molecular structures of organic compounds from the CBSE Class 12 chemistry syllabus.

## Features

- **Interactive 3D Visualization**: View molecules in 3D with realistic bond angles and lengths
- **Animation Controls**: Start/stop rotation, zoom, pan, and reset views
- **Multiple Display Styles**: Stick model, ball & stick, and space-filling representations
- **Comprehensive Database**: All important organic compounds from CBSE Class 12 syllabus
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Educational Information**: Molecular formulas, categories, and descriptions

## Included Compound Categories

### Alcohols
- Methanol, Ethanol, Propanol, Isopropanol, Butanol, Phenol

### Aldehydes
- Formaldehyde, Acetaldehyde, Benzaldehyde

### Ketones
- Acetone, Butanone (MEK)

### Carboxylic Acids
- Formic Acid, Acetic Acid, Benzoic Acid

### Esters
- Methyl Acetate, Ethyl Acetate

### Amines
- Methylamine, Dimethylamine, Aniline

### Hydrocarbons
- **Alkanes**: Methane, Ethane, Propane, Butane
- **Alkenes**: Ethene, Propene
- **Alkynes**: Ethyne
- **Aromatic**: Benzene, Toluene, Naphthalene

### Ethers
- Diethyl Ether

### Haloalkanes
- Chloromethane, Chloroform

## Installation

1. **Clone or download the application**:
   ```bash
   cd organic_chemistry_app
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Browse Compounds**: The home page displays all compounds organized by category
2. **View 3D Structure**: Click on any compound to see its 3D molecular structure
3. **Interact with Molecules**: 
   - **Rotate**: Click and drag with mouse
   - **Zoom**: Use mouse wheel
   - **Pan**: Right-click and drag
4. **Control Animation**: Use the control panel to start/stop rotation
5. **Change Display Style**: Switch between stick, ball & stick, and space-filling models
6. **Toggle Labels**: Show/hide atom labels for better understanding

## Technical Details

### Backend
- **Flask**: Web framework
- **RDKit**: Molecular structure generation and manipulation
- **Python 3.9+**: Required for RDKit compatibility

### Frontend
- **3Dmol.js**: 3D molecular visualization library
- **Bootstrap 5**: Responsive UI framework
- **JavaScript**: Interactive controls and animations

### Molecular Data
- **SMILES Notation**: Used to represent molecular structures
- **3D Coordinates**: Generated using RDKit's embedding algorithms
- **Force Field Optimization**: MMFF (Merck Molecular Force Field) for realistic geometries

## Educational Benefits

- **Visual Learning**: See molecular shapes and bond arrangements in 3D
- **Interactive Exploration**: Rotate and examine molecules from all angles
- **Comparative Study**: Compare different functional groups and their structures
- **CBSE Aligned**: Covers all organic compounds in the Class 12 syllabus

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Troubleshooting

### Common Issues

1. **RDKit Installation Error**:
   - Ensure you have Python 3.9 or higher
   - Try: `conda install -c conda-forge rdkit` if using Anaconda

2. **3D Viewer Not Loading**:
   - Check browser console for JavaScript errors
   - Ensure internet connection for 3Dmol.js CDN

3. **Slow Performance**:
   - Close other browser tabs
   - Try a different browser
   - Reduce animation speed in controls

## Contributing

Feel free to contribute by:
- Adding more compounds
- Improving the UI/UX
- Adding educational content
- Fixing bugs or performance issues

## License

This project is created for educational purposes and is free to use for CBSE Class 12 chemistry education.

## Acknowledgments

- **RDKit**: Open-source cheminformatics toolkit
- **3Dmol.js**: WebGL-based 3D molecular visualization
- **Bootstrap**: Frontend framework
- **CBSE**: Curriculum reference for compound selection
