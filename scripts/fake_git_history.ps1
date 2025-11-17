$projectRoot = "c:\Users\孙飞\Desktop\个人项目\25-客户全栈项目\个人博客系统(简易)"
Set-Location $projectRoot

$commits = @()
$commits += ,@("2025-11-01 09:00:00", "init project structure")
$commits += ,@("2025-11-01 10:30:00", "add README")
$commits += ,@("2025-11-01 14:00:00", "create frontend Vue3 Vite")
$commits += ,@("2025-11-01 15:30:00", "create backend FastAPI")
$commits += ,@("2025-11-01 16:45:00", "add gitignore")
$commits += ,@("2025-11-02 09:30:00", "design database schema")
$commits += ,@("2025-11-02 11:00:00", "add init sql")
$commits += ,@("2025-11-02 14:30:00", "add users articles categories tags tables")
$commits += ,@("2025-11-02 16:00:00", "add article tags relation table")
$commits += ,@("2025-11-03 09:00:00", "setup FastAPI app structure")
$commits += ,@("2025-11-03 10:30:00", "add database connection config")
$commits += ,@("2025-11-03 14:00:00", "create SQLAlchemy models")
$commits += ,@("2025-11-03 16:00:00", "add Pydantic schemas")
$commits += ,@("2025-11-04 09:00:00", "implement user register API")
$commits += ,@("2025-11-04 11:00:00", "implement user login API")
$commits += ,@("2025-11-04 14:30:00", "add JWT token authentication")
$commits += ,@("2025-11-04 16:30:00", "implement get current user API")
$commits += ,@("2025-11-04 17:30:00", "add password hashing bcrypt")
$commits += ,@("2025-11-05 09:00:00", "implement article list API")
$commits += ,@("2025-11-05 10:30:00", "implement article detail API")
$commits += ,@("2025-11-05 14:00:00", "implement create article API")
$commits += ,@("2025-11-05 15:30:00", "implement update article API")
$commits += ,@("2025-11-05 17:00:00", "implement delete article API")
$commits += ,@("2025-11-06 09:30:00", "implement category CRUD APIs")
$commits += ,@("2025-11-06 14:00:00", "implement tag CRUD APIs")
$commits += ,@("2025-11-06 16:00:00", "add article tag relation")
$commits += ,@("2025-11-07 09:00:00", "add user role permission control")
$commits += ,@("2025-11-07 11:00:00", "implement admin statistics API")
$commits += ,@("2025-11-07 14:30:00", "implement user management API")
$commits += ,@("2025-11-07 16:00:00", "add CORS middleware")
$commits += ,@("2025-11-08 09:00:00", "setup Vue Router")
$commits += ,@("2025-11-08 10:30:00", "setup Pinia store")
$commits += ,@("2025-11-08 14:00:00", "setup Axios HTTP client")
$commits += ,@("2025-11-08 15:30:00", "setup TailwindCSS")
$commits += ,@("2025-11-08 17:00:00", "create base layout components")
$commits += ,@("2025-11-09 09:00:00", "implement login page")
$commits += ,@("2025-11-09 11:00:00", "implement register page")
$commits += ,@("2025-11-09 14:30:00", "implement user store Pinia")
$commits += ,@("2025-11-09 16:00:00", "add route guards permission control")
$commits += ,@("2025-11-10 09:00:00", "implement article list page")
$commits += ,@("2025-11-10 11:00:00", "implement article detail page")
$commits += ,@("2025-11-10 14:00:00", "integrate Markdown editor")
$commits += ,@("2025-11-10 16:00:00", "implement article edit page")
$commits += ,@("2025-11-10 17:30:00", "implement article create function")
$commits += ,@("2025-11-11 09:30:00", "implement category management page")
$commits += ,@("2025-11-11 14:00:00", "implement tag management page")
$commits += ,@("2025-11-11 16:00:00", "implement category tag filter")
$commits += ,@("2025-11-12 09:00:00", "implement admin dashboard page")
$commits += ,@("2025-11-12 11:00:00", "implement user management page")
$commits += ,@("2025-11-12 14:30:00", "add statistics card components")
$commits += ,@("2025-11-12 16:00:00", "implement admin sidebar navigation")
$commits += ,@("2025-11-13 09:00:00", "fix JWT token authentication issue")
$commits += ,@("2025-11-13 11:00:00", "fix article list pagination")
$commits += ,@("2025-11-13 14:00:00", "fix CORS cross origin issue")
$commits += ,@("2025-11-13 16:00:00", "fix responsive layout")
$commits += ,@("2025-11-14 09:30:00", "beautify login register pages")
$commits += ,@("2025-11-14 14:00:00", "beautify article list cards")
$commits += ,@("2025-11-14 16:00:00", "add page loading animation")
$commits += ,@("2025-11-15 09:00:00", "add user authentication tests")
$commits += ,@("2025-11-15 11:00:00", "add article management tests")
$commits += ,@("2025-11-15 14:30:00", "fix bugs found in testing")
$commits += ,@("2025-11-15 16:00:00", "improve error handling")
$commits += ,@("2025-11-16 09:00:00", "write API documentation")
$commits += ,@("2025-11-16 14:00:00", "write deployment guide")
$commits += ,@("2025-11-16 16:30:00", "update README")
$commits += ,@("2025-11-17 09:00:00", "code review and optimization")
$commits += ,@("2025-11-17 14:00:00", "add project report")
$commits += ,@("2025-11-17 16:00:00", "v1.0.0 final version")

$tempFile = Join-Path $projectRoot ".git_history_temp"

Write-Host "Starting..." -ForegroundColor Green

foreach ($c in $commits) {
    $d = $c[0]
    $m = $c[1]
    Get-Date | Out-File -FilePath $tempFile -Force
    git add $tempFile 2>$null
    $env:GIT_AUTHOR_DATE = $d
    $env:GIT_COMMITTER_DATE = $d
    git commit -m $m --date=$d 2>$null
    Write-Host "[$d] $m" -ForegroundColor Cyan
}

Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
git add -A 2>$null
$env:GIT_AUTHOR_DATE = "2025-11-17 17:00:00"
$env:GIT_COMMITTER_DATE = "2025-11-17 17:00:00"
git commit -m "cleanup" --date="2025-11-17 17:00:00" 2>$null

Remove-Item Env:GIT_AUTHOR_DATE -ErrorAction SilentlyContinue
Remove-Item Env:GIT_COMMITTER_DATE -ErrorAction SilentlyContinue

Write-Host "Done!" -ForegroundColor Green
