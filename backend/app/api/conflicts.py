from fastapi import APIRouter

from app.reasoning.conflict_detector import scan_all_conflicts

router = APIRouter(prefix="/api/conflicts", tags=["Conflicts"])


@router.get("")
def list_conflicts():
    return scan_all_conflicts()