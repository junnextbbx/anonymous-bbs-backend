from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from database import get_db
from models import Post, Thread
from schemas import ThreadCreate, ThreadResponse

router = APIRouter(prefix="/threads", tags=["threads"])


@router.get("", response_model=list[ThreadResponse])
def list_threads(db: Session = Depends(get_db)):
    """スレッド一覧を新着順で返す。post_count を集計して付与する。"""
    rows = (
        db.query(Thread, func.count(Post.id).label("post_count"))
        .outerjoin(Post, Post.thread_id == Thread.id)
        .group_by(Thread.id)
        .order_by(Thread.created_at.desc())
        .all()
    )

    result = []
    for thread, post_count in rows:
        result.append(
            ThreadResponse(
                id=thread.id,
                title=thread.title,
                created_by=thread.created_by,
                display_name=thread.display_name,
                created_at=thread.created_at,
                post_count=post_count,
            )
        )
    return result


@router.post("", response_model=ThreadResponse, status_code=status.HTTP_201_CREATED)
def create_thread(body: ThreadCreate, db: Session = Depends(get_db)):
    """スレッドを新規作成する。"""
    thread = Thread(title=body.title, created_by=body.created_by, display_name=body.display_name)
    db.add(thread)
    db.commit()
    db.refresh(thread)
    return ThreadResponse(
        id=thread.id,
        title=thread.title,
        created_by=thread.created_by,
        display_name=thread.display_name,
        created_at=thread.created_at,
        post_count=0,
    )
