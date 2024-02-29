from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/all", response_model=List[schemas.Setting])
def read_settings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve settings.
    """
    settings = crud.setting.get_multi(db, skip=skip, limit=limit)

    return settings


@router.get("/", response_model=Any)
def read_settings(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve settings.
    """
    settings = crud.setting.get_multi(db, skip=skip, limit=limit)
    # Format settings to be a dictionary
    # settings_dict = {}
    # for setting in settings:
    #     settings_dict[setting.key] = setting.value
    #     # settings_dict[setting.key] = eval(setting.type)(setting.value)


    def transform_structure(data):
        result = {"path": "", "children": []}

        for entry in data:
            categories = entry.category.split("/")
            current_node = result

            for category in categories:
                if not any(child["path"] == category for child in current_node["children"]):
                    new_node = {"path": category, "children": []}
                    current_node["children"].append(new_node)
                    current_node = new_node
                else:
                    current_node = next(child for child in current_node["children"] if child["path"] == category)

            current_node["key"] = entry.key
            current_node["value"] = entry.value

        return result

    result = transform_structure(settings)

    return result


@router.post("/", response_model=schemas.Setting, status_code=status.HTTP_201_CREATED)
def create_setting(
    *,
    db: Session = Depends(deps.get_db),
    setting_in: schemas.SettingCreate,
) -> Any:
    """
    Create new setting.
    """
    setting = crud.setting.create(db=db, obj_in=setting_in)
    return setting


@router.get("/{id}", response_model=schemas.Setting)
def read_setting(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get setting by ID.
    """
    setting = crud.setting.get(db=db, id=id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.put("/{id}", response_model=schemas.Setting)
def update_setting(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    setting_in: schemas.SettingUpdate,
) -> Any:
    """
    Update an setting.
    """
    setting = crud.setting.get(db=db, id=id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting = crud.setting.update(db=db, db_obj=setting, obj_in=setting_in)
    return setting


@router.delete("/{id}", response_model=schemas.Setting)
def delete_setting(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an setting.
    """
    setting = crud.setting.get(db=db, id=id)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    setting = crud.setting.remove(db=db, id=id)
    return setting
