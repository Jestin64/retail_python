from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.order import OrderCreate, OrderOut
from crud.order import (
    create_order,
    get_orders_by_user,
    update_order_status,
    delete_order,
)
from core.security import get_current_user, admin_required
from models.user import User
from db.session import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

# 1) Place a new order (authenticated user)
@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    summary="Place a new order"
)
def place_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # current_user is injected by get_current_user
    return create_order(db, current_user.id, order_in)

# 2) Get your order history (authenticated user)
@router.get(
    "/",
    response_model=list[OrderOut],
    summary="List current user's orders"
)
def list_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_orders_by_user(db, current_user.id)

# 3) Update order status (admins only)
@router.put(
    "/{order_id}/status",
    response_model=OrderOut,
    summary="Update an order's status (admin only)"
)
def change_order_status(
    order_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    updated = update_order_status(db, order_id, new_status)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

# 4) Cancel (delete) an order (admins only)
@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel an order (admin only)"
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    success = delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return
