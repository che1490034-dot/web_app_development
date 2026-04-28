# 路由設計 (Routes Design) - 旅遊網站系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **主畫面** | GET | `/` | `templates/index.html` | 系統首頁，展示精選景點與導覽 |
| **會員系統** | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| | POST | `/auth/register` | — | 接收註冊資料，存入 DB 後重導向至登入頁 |
| | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| | POST | `/auth/login` | — | 驗證登入資料，成功後重導向至首頁或行程表 |
| | GET | `/auth/logout` | — | 登出並重導向至首頁 |
| **景點功能** | GET | `/places` | `templates/places/index.html` | 顯示所有景點列表 (可搜尋/篩選) |
| | GET | `/places/<id>` | `templates/places/detail.html` | 顯示單一景點詳細介紹與評價 |
| | POST | `/places/<id>/reviews` | — | 接收評價表單，存入 DB 後重導向回景點詳細頁 |
| **行程管理** | GET | `/itineraries` | `templates/itineraries/index.html` | 顯示目前登入使用者的所有行程列表 |
| | GET | `/itineraries/new` | `templates/itineraries/new.html` | 顯示建立新行程表單 |
| | POST | `/itineraries` | — | 建立行程基本資料，存入 DB 後重導向至行程詳細頁 |
| | GET | `/itineraries/<id>` | `templates/itineraries/detail.html` | 顯示單一行程詳細內容與天數規劃 |
| | GET | `/itineraries/<id>/edit`| `templates/itineraries/edit.html` | 顯示編輯行程基本資料的表單 |
| | POST | `/itineraries/<id>/update`| — | 更新行程基本資料 |
| | POST | `/itineraries/<id>/delete`| — | 刪除整筆行程與其項目 |
| **行程項目** | GET | `/itineraries/<id>/items/new`| `templates/itineraries/items_new.html` | 顯示新增景點/活動至行程的表單 |
| | POST | `/itineraries/<id>/items`| — | 將活動項目與預算存入 DB |
| | POST | `/itineraries/<id>/items/<item_id>/delete`| — | 刪除單一行程項目 |
| **分享行程** | GET | `/shared/<code>` | `templates/itineraries/shared.html` | 透過分享碼查看他人行程 (唯讀模式) |

## 2. 每個路由的詳細說明

*(這裡以幾個核心路由為例說明邏輯)*

### 行程列表 `GET /itineraries`
- **輸入**：(無，但需檢查 Session 是否已登入)
- **處理邏輯**：使用 `Itinerary.query.filter_by(user_id=current_user.id).all()` 取得資料。
- **輸出**：渲染 `itineraries/index.html`，將取得的行程列表傳遞給模板。
- **錯誤處理**：未登入時重導向至 `/auth/login`，並顯示 Flash 訊息提示。

### 建立行程 `POST /itineraries`
- **輸入**：表單欄位 `title`, `description`, `start_date`, `end_date`
- **處理邏輯**：驗證欄位不可為空，計算日期合理性。建立 `Itinerary` 實例並存入 DB。
- **輸出**：成功後重導向至 `GET /itineraries/<新產生的id>`。
- **錯誤處理**：驗證失敗時，重新渲染 `itineraries/new.html` 並顯示錯誤訊息。

### 景點詳細頁 `GET /places/<id>`
- **輸入**：URL 參數 `id`
- **處理邏輯**：查詢 `Place.get_by_id(id)`，並透過關聯讀取對應的 `Review` 列表。
- **輸出**：渲染 `places/detail.html`，傳遞景點物件與評價列表。
- **錯誤處理**：若景點 ID 不存在，回傳 404 Not Found 頁面。

## 3. Jinja2 模板清單

所有頁面預設繼承自 `templates/base.html`：
- `base.html` (包含導覽列 Navigation, Flash 訊息顯示區, 頁尾 Footer)
- `index.html` (首頁)
- `auth/register.html` (註冊)
- `auth/login.html` (登入)
- `places/index.html` (景點列表)
- `places/detail.html` (景點介紹)
- `itineraries/index.html` (我的行程列表)
- `itineraries/new.html` (新增行程表單)
- `itineraries/edit.html` (編輯行程基本資料)
- `itineraries/detail.html` (行程詳細頁，含天數、各項活動、總預算計算)
- `itineraries/items_new.html` (新增活動項目與預算表單)
- `itineraries/shared.html` (分享模式下的行程檢視頁)
