from fastapi import APIRouter

from app.api.article_categories import router as articleCategoriesRouter
from app.api.article_tags import router as articleTagsRouter
from app.api.admin import router as adminRouter
from app.api.ai import router as aiRouter
from app.api.articles import router as articlesRouter
from app.api.auth import router as authRouter
from app.api.calendar_events import router as calendarEventsRouter
from app.api.follows import router as followsRouter
from app.api.health import router as healthRouter
from app.api.photos import router as photosRouter
from app.api.quick_notes import router as quickNotesRouter
from app.api.quick_posts import router as quickPostsRouter
from app.api.search import router as searchRouter
from app.api.todos import router as todosRouter
from app.api.users import router as usersRouter


apiRouter = APIRouter()
apiRouter.include_router(adminRouter)
apiRouter.include_router(aiRouter)
apiRouter.include_router(articleCategoriesRouter)
apiRouter.include_router(articleTagsRouter)
apiRouter.include_router(articlesRouter)
apiRouter.include_router(authRouter)
apiRouter.include_router(calendarEventsRouter)
apiRouter.include_router(followsRouter)
apiRouter.include_router(healthRouter)
apiRouter.include_router(photosRouter)
apiRouter.include_router(quickNotesRouter)
apiRouter.include_router(quickPostsRouter)
apiRouter.include_router(searchRouter)
apiRouter.include_router(todosRouter)
apiRouter.include_router(usersRouter)
