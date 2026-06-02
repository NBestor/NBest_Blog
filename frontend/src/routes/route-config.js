export const routes = [
  { path: '/', label: '首页', title: '首页', description: '快写发布、动态流与全局提醒弹窗入口。', visibility: 'public' },
  { path: '/blog', label: '博客', title: '博客文章', description: '公开文章列表页面框架。', visibility: 'public' },
  { path: '/blog/edit', label: '写文章', title: '文章编辑器', description: 'Markdown 编辑器页面框架。', visibility: 'auth' },
  { path: '/blog/draft', label: '草稿', title: '草稿箱', description: '云端草稿管理页面框架。', visibility: 'auth' },
  {
    path: '/blog/detail/sample',
    label: '详情',
    title: '文章详情',
    description: '文章详情、评论、点赞与收藏页面框架。',
    visibility: 'public',
    showInNav: false,
  },
  {
    path: '/quick-posts/sample',
    label: '快写详情',
    title: '快写详情',
    description: '快写正文、点赞和评论详情页。',
    visibility: 'public',
    showInNav: false,
  },
  { path: '/user/login', label: '登录', title: '登录', description: '用户登录页面框架。', visibility: 'guest' },
  { path: '/user/register', label: '注册', title: '注册', description: '用户注册页面框架。', visibility: 'guest' },
  { path: '/user/profile', label: '个人中心', title: '个人中心', description: '资料与内容聚合页面框架。', visibility: 'auth' },
  { path: '/user/setting', label: '设置', title: '个人设置', description: '快写权限与账户设置页面框架。', visibility: 'auth' },
  { path: '/user/follow', label: '关注', title: '关注关系', description: '关注、粉丝与好友列表页面框架。', visibility: 'auth' },
  { path: '/photo', label: '照片墙', title: '照片墙', description: '照片资源展示与管理页面框架。', visibility: 'public' },
  { path: '/todo', label: '待办', title: '待办清单', description: 'TodoList 与到期提醒页面框架。', visibility: 'auth', showInNav: false },
  { path: '/calendar', label: '日历', title: '日历备忘录', description: '生日、纪念日与年度重复页面框架。', visibility: 'auth', showInNav: false },
  { path: '/quick/note', label: '快记', title: '私密快记', description: '仅自己可见的快记页面框架。', visibility: 'auth' },
  { path: '/admin', label: '管理', title: '管理', description: '管理员用户与内容治理。', visibility: 'admin' },
];

export const privatePaths = new Set(
  routes.filter((route) => route.visibility === 'auth' || route.visibility === 'admin').map((route) => route.path),
);
