"""Chapter API 路由"""
from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from pydantic import BaseModel, Field

from application.services.chapter_service import ChapterService
from application.dtos.chapter_dto import ChapterDTO
from interfaces.api.dependencies import get_chapter_service
from domain.shared.exceptions import EntityNotFoundError


router = APIRouter(prefix="/novels", tags=["chapters"])


# Request Models
class UpdateChapterContentRequest(BaseModel):
    """更新章节内容请求"""
    content: str = Field(..., min_length=0, max_length=100000, description="章节内容")


# Routes
@router.get("/{novel_id}/chapters", response_model=List[ChapterDTO])
async def list_chapters(
    novel_id: str,
    service: ChapterService = Depends(get_chapter_service)
):
    """列出小说的所有章节

    Args:
        novel_id: 小说 ID
        service: Chapter 服务

    Returns:
        章节 DTO 列表
    """
    return service.list_chapters_by_novel(novel_id)


@router.get("/{novel_id}/chapters/{chapter_number}", response_model=ChapterDTO)
async def get_chapter(
    novel_id: str,
    chapter_number: int = Path(..., gt=0, description="章节编号"),
    service: ChapterService = Depends(get_chapter_service)
):
    """获取章节详情

    Args:
        novel_id: 小说 ID
        chapter_number: 章节号
        service: Chapter 服务

    Returns:
        章节 DTO

    Raises:
        HTTPException: 如果章节不存在
    """
    chapter = service.get_chapter_by_novel_and_number(novel_id, chapter_number)
    if chapter is None:
        raise HTTPException(
            status_code=404,
            detail=f"Chapter not found: {novel_id}/chapter-{chapter_number}"
        )
    return chapter


@router.put("/{novel_id}/chapters/{chapter_number}", response_model=ChapterDTO)
async def update_chapter(
    novel_id: str,
    request: UpdateChapterContentRequest,
    chapter_number: int = Path(..., gt=0, description="章节编号"),
    service: ChapterService = Depends(get_chapter_service)
):
    """更新章节内容

    Args:
        novel_id: 小说 ID
        chapter_number: 章节号
        request: 更新内容请求
        service: Chapter 服务

    Returns:
        更新后的章节 DTO

    Raises:
        HTTPException: 如果章节不存在
    """
    try:
        return service.update_chapter_by_novel_and_number(
            novel_id,
            chapter_number,
            request.content
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
