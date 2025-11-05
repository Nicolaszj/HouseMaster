"""
FastAPI para HouseMaster
API REST JSON de propiedades usando FastAPI
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from pydantic import BaseModel
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HouseMaster.settings')
django.setup()

from property.models import Property
from django.contrib.auth.models import User

app = FastAPI(
    title="HouseMaster API",
    description="API REST para gestión de propiedades inmobiliarias",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class AgentInfo(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

class PropertyResponse(BaseModel):
    id: int
    title: str
    description: str
    type: str
    status: str
    price: float
    rooms: int
    bathrooms: int
    area: float
    location: str
    address: str
    city: str
    department: str
    agent: AgentInfo
    url: str
    image_url: Optional[str]
    created_at: str

class PropertiesListResponse(BaseModel):
    count: int
    properties: List[PropertyResponse]
    filters_applied: dict

# Endpoints
@app.get("/", tags=["Info"])
async def root():
    """Información de la API"""
    return {
        "message": "HouseMaster API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "properties": "/api/properties/",
            "properties_for_sale": "/api/properties/for-sale/",
        }
    }

@app.get("/api/properties/", response_model=PropertiesListResponse, tags=["Properties"])
def get_properties(
    type: Optional[str] = Query(None, description="Filtrar por tipo: 'Venta' o 'Arriendo'"),
    status: Optional[str] = Query(None, description="Filtrar por estado: 'Disponible', 'Vendida', 'Arrendada'"),
    min_price: Optional[float] = Query(None, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, description="Precio máximo"),
    city: Optional[str] = Query(None, description="Filtrar por ciudad"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados")
):
    """
    Obtener lista de propiedades con filtros opcionales
    
    - **type**: Tipo de propiedad (Venta/Arriendo)
    - **status**: Estado de la propiedad
    - **min_price**: Precio mínimo
    - **max_price**: Precio máximo
    - **city**: Ciudad
    - **limit**: Cantidad máxima de resultados (1-100)
    """
    queryset = Property.objects.all()
    
    # Aplicar filtros
    if type:
        queryset = queryset.filter(type=type)
    if status:
        queryset = queryset.filter(status=status)
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)
    if city:
        queryset = queryset.filter(city__icontains=city)
    
    # Limitar resultados
    queryset = queryset[:limit]
    
    # Construir respuesta
    properties_data = []
    for prop in queryset:
        agent_data = AgentInfo(
            id=prop.agent.id,
            username=prop.agent.username,
            email=prop.agent.email,
            full_name=f"{prop.agent.first_name} {prop.agent.last_name}".strip() or prop.agent.username
        )
        
        property_data = PropertyResponse(
            id=prop.id,
            title=prop.title,
            description=prop.description,
            type=prop.type,
            status=prop.status,
            price=float(prop.price),
            rooms=prop.rooms,
            bathrooms=prop.bathrooms,
            area=float(prop.area),
            location=f"{prop.city}, {prop.department}",
            address=prop.address,
            city=prop.city,
            department=prop.department,
            agent=agent_data,
            url=f"http://localhost:8000/es/property/{prop.id}/",
            image_url=f"http://localhost:8000{prop.image.url}" if prop.image else None,
            created_at=prop.created_at.isoformat()
        )
        properties_data.append(property_data)
    
    return PropertiesListResponse(
        count=len(properties_data),
        properties=properties_data,
        filters_applied={
            "type": type,
            "status": status,
            "min_price": min_price,
            "max_price": max_price,
            "city": city,
            "limit": limit
        }
    )

@app.get("/api/properties/for-sale/", tags=["Properties"])
def get_properties_for_sale(
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados")
):
    """
    Obtener propiedades en venta disponibles
    
    - **limit**: Cantidad máxima de resultados (1-100)
    """
    queryset = Property.objects.filter(type="Venta", status="Disponible")[:limit]
    
    properties_data = []
    for prop in queryset:
        properties_data.append({
            "id": prop.id,
            "title": prop.title,
            "price": float(prop.price),
            "rooms": prop.rooms,
            "bathrooms": prop.bathrooms,
            "area": float(prop.area),
            "location": f"{prop.city}, {prop.department}",
            "url": f"http://localhost:8000/es/property/{prop.id}/",
            "image_url": f"http://localhost:8000{prop.image.url}" if prop.image else None
        })
    
    return {
        "count": len(properties_data),
        "properties_for_sale": properties_data
    }

@app.get("/api/properties/{property_id}", response_model=PropertyResponse, tags=["Properties"])
def get_property_detail(property_id: int):
    """
    Obtener detalles de una propiedad específica
    
    - **property_id**: ID de la propiedad
    """
    try:
        prop = Property.objects.get(id=property_id)
        
        agent_data = AgentInfo(
            id=prop.agent.id,
            username=prop.agent.username,
            email=prop.agent.email,
            full_name=f"{prop.agent.first_name} {prop.agent.last_name}".strip() or prop.agent.username
        )
        
        return PropertyResponse(
            id=prop.id,
            title=prop.title,
            description=prop.description,
            type=prop.type,
            status=prop.status,
            price=float(prop.price),
            rooms=prop.rooms,
            bathrooms=prop.bathrooms,
            area=float(prop.area),
            location=f"{prop.city}, {prop.department}",
            address=prop.address,
            city=prop.city,
            department=prop.department,
            agent=agent_data,
            url=f"http://localhost:8000/es/property/{prop.id}/",
            image_url=f"http://localhost:8000{prop.image.url}" if prop.image else None,
            created_at=prop.created_at.isoformat()
        )
    except Property.DoesNotExist:
        return {"error": "Property not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
