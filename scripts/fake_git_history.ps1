# 虚构 Gi提交记录生成脚本
#用法 在根录运行此脚本# 注意: 运行前请确保已经 gi it并且有初始提交

# 设置 UTF-8 编码
[Cnsol]::OupuEndng = [Sytem.Text.Encoding]::UTF8
$env:LC_ALL"C.UTF-8"

# 提交记录列表 按时间顺序，从早到晚
    @{ date = ;msag = 初始化项目结构，创建前后端目录" },    @{ dae;messge= "添加 .d项目说明文档}
@{ da40;mssg配置. 忽略规则 },    
    # 后端开发
    @{ dae0;msae= "后端: 初始化 FtAPI项目结构 },    @{ dae;messge=后端: 添加数据库配置和连接模块" },    @{ dae;m= "后端: 创建用户模型 (UerModl" },    @{ dae;messg="后端:实现用户注册接口 },    @{ dae3;mesag = "后端:实现用户登录接口和JWT认证 },    @{ dae1:;messg ="后端:添加密码加密工具函数 },    @{ dae;mssg = "后端: 创建文章模型(rticM) },    @{ dae3"; message = "后端: 实现文章 CRUD 接口 }
   @{;sag = "后端: 创建分类模型(CatoyModel) },    @{ dae03;sag ="后端:实现分类管理接口 },    @{ dae0; message =后端: 创建标签模型(agMdl)" },
    @{d5;ssa="后端:实现标签管理接口 },    @{ dae0;mee = "后端:添加文章-标签多对多关联 },    @{ dae;ssg=后端:实现文章分页查询功能"}
@{ e1;ssg=后端: 添加用户权限验证中间件" },    @{ dae4;ssg=后端: 实现管理员统计数据接口" },    @{ dae6;ssag="后端:配置 CORS 跨域支持 },    
    # 数据库
    @{ dae0;sse=数据库: 创建初始化 SQL 脚本" },    @{ dae03;sse数据库 添加测试数据和默认账户 }

    # 前端开发
    @{ de;messge= "前端: 初始化 V3+TyScp 项目 },    @{ dae03;ssag="前端: 配置 TlwndCSS样式框架 },    @{ dae0;s = "前端: 配置 Vu Rouer路由 },    @{ dae;messge="前端: 配置 Pni 状态管理 },    @{ dae;mesag = "前端:封装Axis 请求工具 },    @{ dae1:;mesag = "前端:创建用户认证S },    @{ dae3;mesag="前端:实现登录页面组件 },    @{ dae6;mesag = "前端:实现注册页面组件 },    @{ dae909;mssg = "前端: 创建主布局组件(MinL) },    @{ dae11;ss = "前端: 实现顶部导航栏组件 },    @{ dae4;s = "前端: 实现文章列表页面 },    @{ dae6;sag ="前端:实现文章卡片组件 },    @{ dae10 ; message =前端:集成Mkw编辑器 },    @{ dae113;s = "前端: 实现文章编辑页面 },    @{ dae4;ssg ="前端:实现文章详情页面 },    @{ dae6;mssg= "前端: 添加 渲染支持 },    @{ dae 09;ss前端 实现分类管理页面 }
 @{ d110;ss= 前端: 实现标签管理页面" },    @{ dae3;sse= "前端: 创建后台管理布局 (AdiLyou" },    @{ dae;sse=前端: 实现管理员控制台页面" },    @{ dae;s = 前端: 实现用户管理页面" },    @{ dae;s= 前端: 添加路由守卫和权限控制" },    @{ dae0;meg = 前端: 优化页面响应式布局" },    @{ dae3;ssag="前端:添加加载状态和错误提示 },    
    # 功能完善 
    @{ dae;mag = 功能: 实现文章状态切换 (草稿/发布" },    @{ dae;messg ="功能:添加文章浏览量统计 },
    
    
        @{ dae3;meage ="功能:实现分类筛选功能 },   
        
        
         @{ dae;mag = "功能:实现标签筛选功能 }, 
         
         
            @{ dae0;mssge = "修复: 解决 JWTTke 类型转换问题" },
    @{da = "2025-11-14 11:00:00";mess = "修复: 解决跨域请求携带凭证问题 }, 
    
    
       @{ dae;mssg ="优化:改进表单验证提示信息 },    @{ dae;mess = "优化: 统一API错误响应格式 },
    
    # 测试和文档    @{ dae;mesag ="测试:完成用户认证模块测试 },    @{ dae;ess = "测试:完成文章管理模块测试 },    @{ dae0"; message = "测试: 完成权限控制功能测试 }
@{da;essag=文档: 编写 API 接口文档" },    @{ dae;mssage="文档: 编写项目部署说明" },
    @{ e = 2025-11-16 11:00:00"; esage"文档: 完成项目报告初稿" }
    { date = ;ssa = 文档: 补充数据库设计说明" },    @{ dae0;messg= 文档: 完善项目报告内容" },    
    # 最终完善
    @{ dae;mssag="优化: 改进页面加载性能" },
    @{ de = 2025-11-17 11:00:00"; esage"优化: 完善错误处理机制" }
    { date = ;messg= 完成: 项目功能开发完毕" },    @{ dae;message = 发布: 正式版本" }
)

Wrte-Host "========================================" -ForegroudCoorCyan
Wite-Hot "  虚构 Gt 提交记录生成脚本" -FregroudColor CyanWri-Host"======================================="-FregroudColor Cyn
Wrie-Host""
Wie-Hs即将创建 $($comm.Coun) 条提交记录" -ForegroundCol Yllow按任意键开始，或按 Cl+C 取消 Yellow
$null =$Host.UI.RawUI.ReadKey("NoEcho,IncludKyDow")

# 创建一个临时文件用于触发提交
$tempFile = ".git_history_temp"ommitateommit.dateessageommit.message
    
    # 修改临时文件内容  $timestamp=ate -Format "yyyy-MM-dd HH:mm:ss"
    "$messge - $imstamp"Encoding UT8
    
    # 添加文件到暂存区
    
    #设置提交日期并提交ateate
    essage"ate"
    OK] ate -essageGree
# 删除临时文件清理: 移除临时文件
# 清除环境变量
Write-Host """======================================== -ForegroundColr Cya
Writ-Host "  完成 共创建 $($commits.Count + 1) 条提交记录reen
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Wite-Host "提示: 运行 'git log --onelin' 查看提交历史" -ForgroudColor Yellow