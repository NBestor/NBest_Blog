## ADDED Requirements

### Requirement: Upload Image Button Visible Label
文章编辑器（`BlogEditPage.jsx`）中 `.article-tool-row` 区域的文件上传按钮 SHALL 显示可见文字标签"上传图片"，并 SHALL 保留 `title` 属性提供悬停提示。点击该按钮 MUST 触发文件选择对话框，选择图片后 SHALL 自动将图片以 Markdown 格式插入正文末尾。

#### Scenario: 按钮显示文字标签
- **WHEN** 用户打开文章编辑器（新建草稿或编辑已有文章）
- **THEN** `.article-tool-row` 中「上传图片」按钮上显示文字"上传图片"（visible）

#### Scenario: 悬停显示 tooltip
- **WHEN** 用户鼠标悬停在「上传图片」按钮上
- **THEN** 浏览器显示 tooltip：「选择图片文件，上传后将自动插入到正文末尾」

#### Scenario: 点击上传图片
- **WHEN** 用户点击「上传图片」按钮
- **THEN** 浏览器弹出文件选择对话框，限定接受 `image/png, image/jpeg, image/webp` 格式

#### Scenario: 上传后插入正文
- **WHEN** 用户选择有效图片文件并确认
- **THEN** 图片上传到服务器后，正文末尾自动追加 `![图片](http://127.0.0.1:8000/static/images/...)` Markdown 代码，并提示「图片已插入正文」

#### Scenario: 上传失败时提示
- **WHEN** 用户选择无效格式或其他原因上传失败
- **THEN** 页面提示「图片上传失败，请选择 jpg、png 或 webp 图片」