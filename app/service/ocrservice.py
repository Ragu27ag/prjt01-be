from typing import Dict, List, Union
from app.schema import ImageData
import easyocr
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import httpx
import re


async def identify_gender(imageData : ImageData) -> Dict[str,Union[List[str],bool]] : 
 try:
        image_url = imageData.image_url
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
        img = Image.open(BytesIO(response.content))


    
        img_np = np.array(img)


        reader = easyocr.Reader(['en'])  

        result = reader.readtext(img_np, detail=0)

        extracted_texts = []
        print("Extracted Text:")
        for line in result:
            print(line)
            extracted_texts.append(line)
        
        print('extracted_texts :',extracted_texts)
        
        isFemale = False
        isAdhaar = False
        
        identifier = ['aadhaar','female']
        lower_extracted_texts = [word.lower() if isinstance(word,str) and not  word.isdigit() else word for word in extracted_texts ]
        print('lower_extracted_texts',lower_extracted_texts)

        aadhaar_pattern = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b')

        aadhaar_numbers = [match.group() for text in lower_extracted_texts for match in aadhaar_pattern.finditer(text)]

        print("Extracted Aadhaar number(s):", aadhaar_numbers)

        missing = [word.lower() for word in identifier if word.lower() not in lower_extracted_texts ]
        print('missing',missing)
        if not missing :
            isFemale = True
            isAdhaar = True
        elif 'aadhaar' in missing and 'female' in missing :
            isFemale = False
            isAdhaar = False
        elif 'aadhaar' in missing  :
            isFemale = True
            isAdhaar = False
        elif 'female' in missing  :
            isFemale = False
            isAdhaar = True
            
        
        return {'extracted_texts' : extracted_texts,
                'isFemale' : isFemale,
                'isAdhaar':isAdhaar,
                'addhaar_number' : aadhaar_numbers[0],
                'error':None}
 except Exception as e :
     return {'error':str(e)}
     