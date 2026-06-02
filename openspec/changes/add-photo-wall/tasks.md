## 1. 现状差异检查

- [x] 1.1 检查 `backend/app/db/database.py`：确认 `photos` 表字段、可见范围取值和索引满足照片墙规格，必要时补充索引或约束。
- [x] 1.2 检查 `backend/app/schemas/photo.py`：确认响应字段覆盖 `id/user_id/author_nickname/url/source_type/visible_type/upload_time/can_manage`，并保留可见范围校验。
- [x] 1.3 检查 `backend/app/api/users.py` 和 `backend/app/api/articles.py`：确认头像上传和 Markdown 文章插图上传都会创建照片墙记录。
- [x] 1.4 检查 `frontend/src/pages/PhotoPage.jsx` 和 `frontend/src/styles/global.css`：确认当前照片墙缺口，记录需要补齐的复制链接、管理态和游客态 UI。

## 2. 后端权限与文件处理收敛

- [x] 2.1 修改 `backend/app/services/photo_service.py`：统一照片可管理判断，支持拥有者和管理员，并让 `can_manage` 来源于后端权限判断。
- [x] 2.2 修改 `backend/app/services/photo_service.py`：调整照片列表查询，使游客只看公开照片，登录用户看公开照片和自己的照片，管理员可管理全站可返回的照片。
- [x] 2.3 修改 `backend/app/services/photo_service.py`：强化删除本地文件的路径安全，只删除静态上传目录内的文件。
- [x] 2.4 修改 `backend/app/api/photos.py`：让修改可见性和删除接口传入当前用户角色，非拥有者且非管理员返回 404。
- [x] 2.5 如检查发现缺失，修改 `backend/app/db/database.py`：补充 `idx_photos_visible_type` 或其他必要索引。

## 3. 前端照片墙交互补齐

- [x] 3.1 修改 `frontend/src/pages/PhotoPage.jsx`：新增复制图片链接能力，优先调用剪贴板，失败时显示可手动复制的链接或提示。
- [x] 3.2 修改 `frontend/src/pages/PhotoPage.jsx`：在照片预览弹窗中显示复制链接入口、来源、可见范围和关闭操作。
- [x] 3.3 修改 `frontend/src/pages/PhotoPage.jsx`：确保游客不显示上传、删除、可见范围修改和复制管理区之外的操作。
- [x] 3.4 修改 `frontend/src/pages/PhotoPage.jsx`：确保登录用户只对 `can_manage` 为真的照片看到删除、复制链接和可见范围修改入口。
- [x] 3.5 修改 `frontend/src/styles/global.css`：补充复制链接、预览信息、管理操作和移动端照片网格样式。

## 4. 后端验证

- [x] 4.1 运行后端 API 验证：游客 `GET /api/photos` 只返回公开照片。
- [x] 4.2 运行后端 API 验证：登录用户可上传合法图片，非法图片被拒绝，游客上传被拒绝。
- [x] 4.3 运行后端 API 验证：登录用户可看到自己的私密照片，其他普通用户看不到该私密照片。
- [x] 4.4 运行后端 API 验证：照片拥有者可修改可见范围，非拥有者不可修改。
- [x] 4.5 运行后端 API 验证：照片拥有者可删除照片，非拥有者不可删除，删除后列表不再返回。
- [x] 4.6 运行后端 API 验证：头像上传和文章图片上传会创建照片墙记录。
- [x] 4.7 如已有管理员账号或可创建管理员，运行后端 API 验证：管理员可修改和删除可管理照片。

## 5. 前端验证

- [x] 5.1 运行 `npm run lint`。
- [x] 5.2 运行 `npm run build`。
- [x] 5.3 使用 in-app browser 验证游客 `/photo`：只显示公开照片，不显示上传、删除或可见性修改入口。
- [x] 5.4 使用 in-app browser 验证登录用户 `/photo`：上传入口、照片预览、复制链接、可见性修改和删除操作可见且可用。
- [x] 5.5 使用 in-app browser 验证私密隔离：用户 A 的私密照片不出现在用户 B 或游客的照片墙中。

## 6. OpenSpec 收尾

- [x] 6.1 运行 `openspec validate add-photo-wall --strict`。
- [x] 6.2 确认 `openspec/changes/add-photo-wall/tasks.md` 所有实现与验证项完成。
