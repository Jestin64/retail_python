from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from core.security import get_current_user, admin_required
from crud.order import create_order, get_user_orders, get_all_orders, update_order_status
from schemas.order import OrderCreate, OrderOut
from models.user import User
from models.order import OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])

# Customer: Place order
@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def place_order(order_data: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return create_order(db, user.id, order_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Customer: View my orders
@router.get("/me", response_model=List[OrderOut])
def my_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_user_orders(db, user.id)

# Admin: View all orders
@router.get("/", response_model=List[OrderOut])
def admin_get_all_orders(db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    return get_all_orders(db)

# Admin: Update order status
@router.put("/{order_id}", response_model=OrderOut)
def admin_update_order(order_id: int, status: OrderStatus, db: Session = Depends(get_db), admin: User = Depends(admin_required)):
    updated = update_order_status(db, order_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated
