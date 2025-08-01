from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from predict import predict_polymer_properties
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, Draw
from pubchempy import get_compounds
import re
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()

# ✅ Add your deployed frontend domain here
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://transpolymer.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    smiles: str  # SMILES string input

class PolymerNameRequest(BaseModel):
    polymer_name: str

class PredictResponse(BaseModel):
    results: dict  # Predicted properties from predict_polymer_properties
    molecular_weight: float  # Molecular weight of the polymer
    structure_image: str  # Base64-encoded image of the polymer structure

class PolymerNameResponse(BaseModel):
    smiles: str
    molecular_weight: float
    structure_image: str

def calculate_molecular_weight(smiles: str) -> float:
    """Calculate the molecular weight of a molecule from its SMILES string."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError("Invalid SMILES string")
        # Calculate the exact molecular weight
        mw = Descriptors.MolWt(mol)
        return mw
    except Exception as e:
        raise ValueError(f"Failed to calculate molecular weight: {str(e)}")

def generate_structure_image(smiles: str) -> str:
    """Generate a 2D structure image of the molecule as a base64-encoded string."""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError("Invalid SMILES string")
        
        # Generate 2D coordinates for visualization
        AllChem.Compute2DCoords(mol)
        
        # Draw the molecule
        img = Draw.MolToImage(mol, size=(300, 300))
        
        # Convert the image to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"
    except Exception as e:
        raise ValueError(f"Failed to generate structure image: {str(e)}")

def polymer_name_to_smiles(polymer_name: str):
    """Convert polymer name to SMILES string with improved error handling."""
    try:
        # Clean the polymer name
        name = polymer_name.lower().strip()
        original_name = name
        
        # Handle specific polymer name variations first
        polymer_name_fixes = {
            'polythene': 'polyethylene',
            'polythylene': 'polyethylene',
            'polyvinyl chloride': 'poly(vinyl chloride)',
            'pvc': 'poly(vinyl chloride)',
            'pet': 'poly(ethylene terephthalate)',
            'ptfe': 'polytetrafluoroethylene',
            'teflon': 'polytetrafluoroethylene',
            'nylon': 'caprolactam',
            'nylon 6': 'caprolactam',
            'nylon-6': 'caprolactam'
        }
        
        # Apply name fixes
        if name in polymer_name_fixes:
            name = polymer_name_fixes[name]
        
        # Remove poly prefix more carefully
        processed_names = []
        
        # Try multiple variations of name processing
        if name.startswith('poly'):
            # Remove "poly" prefix carefully
            monomer_name = re.sub(r'^poly\s*', '', name)
            # Remove parentheses and brackets
            monomer_name = re.sub(r'^[\(\[]', '', monomer_name)
            monomer_name = re.sub(r'[\)\]]$', '', monomer_name)
            processed_names.append(monomer_name)
            
            # Also try the full name
            processed_names.append(name)
        else:
            processed_names.append(name)
        
        # Add original name as fallback
        processed_names.append(original_name)
        processed_names.append(polymer_name.lower().strip())
        
        # Remove duplicates while preserving order
        seen = set()
        processed_names = [x for x in processed_names if not (x in seen or seen.add(x))]
        
        # Common polymer name mappings (monomer names to SMILES)
        polymer_mappings = {
            'ethylene': 'CC',
            'propylene': 'CCC', 
            'styrene': 'c1ccc(cc1)C=C',
            'vinyl chloride': 'C=CCl',
            'methyl methacrylate': 'C=C(C)C(=O)OC',
            'ethylene glycol': 'OCCO',
            'terephthalic acid': 'O=C(O)c1ccc(cc1)C(=O)O',
            'adipic acid': 'O=C(O)CCCCC(=O)O',
            'caprolactam': 'O=C1CCCCCN1',
            'acrylonitrile': 'C=CC#N',
            'butadiene': 'C=CC=C',
            'isoprene': 'C=C(C)C=C',
            'tetrafluoroethylene': 'C(F)(F)=C(F)F',
            # Add direct polymer mappings
            'polyethylene': 'CC',
            'polypropylene': 'CCC',
            'polystyrene': 'c1ccc(cc1)C=C',
            'poly(vinyl chloride)': 'C=CCl',
            'poly(methyl methacrylate)': 'C=C(C)C(=O)OC',
            'polyacrylonitrile': 'C=CC#N',
            'polybutadiene': 'C=CC=C',
            'polyisoprene': 'C=C(C)C=C',
            'polytetrafluoroethylene': 'C(F)(F)=C(F)F'
        }
        
        # Check all processed names against mappings
        for processed_name in processed_names:
            if processed_name in polymer_mappings:
                print(f"Found mapping for '{processed_name}': {polymer_mappings[processed_name]}")
                return polymer_mappings[processed_name]
        
        # Try PubChem lookup with all processed names
        for processed_name in processed_names:
            try:
                print(f"Trying PubChem lookup for: '{processed_name}'")
                compounds = get_compounds(processed_name, 'name', timeout=10)
                
                if compounds and len(compounds) > 0:
                    compound = compounds[0]
                    
                    # Get canonical or isomeric SMILES
                    smiles = compound.canonical_smiles or compound.isomeric_smiles
                    
                    if smiles:
                        # Validate the SMILES
                        mol = Chem.MolFromSmiles(smiles)
                        if mol is not None:
                            print(f"Found SMILES from PubChem for '{processed_name}': {smiles}")
                            return smiles
                
            except Exception as pubchem_error:
                print(f"PubChem lookup failed for '{processed_name}': {str(pubchem_error)}")
                continue
        
        print(f"No SMILES found for any variation of: {processed_names}")
        return None
        
    except Exception as e:
        print(f"Error converting polymer name: {str(e)}")
        return None

@app.post("/polymer-to-smiles", response_model=PolymerNameResponse)
async def convert_polymer_name(request: PolymerNameRequest):
    """Convert polymer name to SMILES and return molecular info."""
    try:
        smiles = polymer_name_to_smiles(request.polymer_name)
        if not smiles:
            raise HTTPException(
                status_code=404, 
                detail=f"Polymer '{request.polymer_name}' not found or conversion failed. "
                       "Try using a more specific monomer name (e.g., 'styrene' instead of 'polystyrene')"
            )
        
        # Calculate molecular weight
        mw = calculate_molecular_weight(smiles)
        
        # Generate structure image
        structure_image = generate_structure_image(smiles)
        
        return {
            "smiles": smiles,
            "molecular_weight": mw,
            "structure_image": structure_image
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """Predict polymer properties from SMILES string."""
    try:
        # Validate SMILES
        mol = Chem.MolFromSmiles(request.smiles)
        if mol is None:
            raise ValueError("Invalid SMILES string")
        
        # Get predicted properties
        results = predict_polymer_properties(request.smiles)
        
        # Calculate molecular weight
        mw = calculate_molecular_weight(request.smiles)
        
        # Generate structure image
        structure_image = generate_structure_image(request.smiles)
        
        return {
            "results": results,
            "molecular_weight": mw,
            "structure_image": structure_image
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Polymer Prediction API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "Polymer Prediction API",
        "endpoints": ["/predict", "/polymer-to-smiles"]
    }