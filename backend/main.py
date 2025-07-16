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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Adjust if deployed
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
    try:
        # Clean the polymer name
        name = polymer_name.lower().strip()
        
        # Remove common prefixes
        name = re.sub(r'^poly', '', name)
        
        # Try to get from PubChem
        compounds = get_compounds(name, 'name')
        
        if compounds:
            # Get the first compound and convert to SMILES
            compound = compounds[0]
            mol = Chem.MolFromSmiles(compound.isomeric_smiles)
            
            if mol:
                # Try to polymerize the monomer
                polymer_smiles = AllChem.ReplaceSubstructs(
                    mol, 
                    Chem.MolFromSmiles('[*]'), 
                    Chem.MolFromSmiles('[*]'), 
                    replaceAll=True
                )
                if polymer_smiles:
                    return Chem.MolToSmiles(polymer_smiles[0])
        
        # Fallback to simple SMILES if polymerization fails
        if compounds:
            return compounds[0].isomeric_smiles
        
        return None
        
    except Exception as e:
        print(f"Error converting polymer name: {str(e)}")
        return None

@app.post("/polymer-to-smiles", response_model=PolymerNameResponse)
async def convert_polymer_name(request: PolymerNameRequest):
    try:
        smiles = polymer_name_to_smiles(request.polymer_name)
        if not smiles:
            raise HTTPException(status_code=404, detail="Polymer not found or conversion failed")
        
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
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