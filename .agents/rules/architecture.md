---
trigger: always_on
---

# Laya Architecture Rules

When adding or modifying code in `this folder`, strictly follow these architectural standards:

## 1. Directory Structure & Alignment
Maintain parallel domain folders across the three layers:
- `controllers/<domain>/`:
  - `<domain>_controller.py`: APIRouter definitions & endpoint handlers.
  - `<domain>_types.py`: Pydantic request & response models.
  - `__init__.py`: exports `<domain>_router`.
- `services/<domain>/`:
  - `<domain>_service.py`: Barrel file grouping and exposing domain usecase functions.
  - `__init__.py`: exports the service functions.
- `usecases/<domain>/`:
  - 1 function = 1 file: `<action_name>_usecase.py`.
  - `__init__.py`: exports the usecase functions.

## 2. Dependency Direction
- Controllers depend on Services and Types.
- Services re-export and coordinate Usecases.
- Usecases contain business logic and interact with the Laya Router.
- Usecases must NEVER import FastAPI, Request, Response, or HTTP-specific exceptions.

## 3. Asynchronous & Threading Rules
- CPU inference in PyTorch is synchronous and blocking.
- Controllers must always delegate synchronous usecase execution using `await asyncio.to_thread(func, *args)`.

## 4. Router Singleton
- Always obtain the Laya Router through `get_laya_router()` from `usecases.predict.get_laya_router_usecase` to prevent duplicate loading of ModernBERT weights into memory.
