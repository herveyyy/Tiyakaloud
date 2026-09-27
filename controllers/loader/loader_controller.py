import asyncio
from fastapi import APIRouter, HTTPException
from controllers.loader.loader_types import (
    LoadModelRequest,
    LoadModelResponse,
    UnloadModelRequest,
    UnloadModelResponse,
    ModelStatusResponse,
    CustomPresetRequest,
    CustomPresetResponse,
    PresetsListResponse,
)
from services.loader import (
    load_model,
    unload_model,
    get_model_status,
    load_custom_preset,
    get_presets,
)

router = APIRouter(prefix="/models", tags=["Model Lifecycle & Custom Loader"])


@router.get("", response_model=ModelStatusResponse)
async def status():
    """Inspect current model status: shows registered and active in-memory models."""
    try:
        return await asyncio.to_thread(get_model_status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load", response_model=LoadModelResponse)
async def load(req: LoadModelRequest):
    """Dynamically warm up or register and load a standard or custom HuggingFace model."""
    try:
        return await asyncio.to_thread(
            load_model,
            req.model_name,
            custom_repo=req.custom_repo,
            subfolder=req.subfolder,
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unload", response_model=UnloadModelResponse)
async def unload(req: UnloadModelRequest):
    """Evict loaded model weights from memory to reclaim RAM/VRAM."""
    try:
        return await asyncio.to_thread(unload_model, model_name=req.model_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/presets", response_model=PresetsListResponse)
async def list_presets():
    """List all built-in and dynamically registered custom question presets."""
    try:
        return await asyncio.to_thread(get_presets)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/presets", response_model=CustomPresetResponse)
async def create_preset(req: CustomPresetRequest):
    """Register a custom questions preset for rapid and consistent decision queries."""
    try:
        return await asyncio.to_thread(load_custom_preset, req.preset_name, req.questions)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
