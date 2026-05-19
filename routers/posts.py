from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from database import get_db
from models import Post, Thread
from schemas import PostCreate, PostResponse

router = APIRouter(prefix="/threads/{thread_id}/posts", tags=["posts"])


def get_thread_or_404(thread_id: int, db: Session) -> Thread:
    thread = db.get(Thread, thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread


@router.get("", response_model=list[PostResponse])
def list_posts(thread_id: int, db: Session = Depends(get_db)):
    """指定スレッドの投稿一覧を昇順で返す。"""
    get_thread_or_404(thread_id, db)
    return (
        db.query(Post)
        .filter(Post.thread_id == thread_id)
        .order_by(Post.created_at.asc())
        .all()
    )


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(thread_id: int, body: PostCreate, db: Session = Depends(get_db)):
    """指定スレッドに投稿を作成する。"""
    get_thread_or_404(thread_id, db)
    post = Post(thread_id=thread_id, body=body.body, created_by=body.created_by, display_name=body.display_name)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
