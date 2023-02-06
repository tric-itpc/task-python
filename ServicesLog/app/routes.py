from app import views

def setup_routes(app):
    app.router.add_view("/add", views.AddService)
    app.router.add_view("/monitor/start", views.StartMonitor)
    app.router.add_view("/monitor/stop", views.StartMonitor)
    app.router.add_view("/history", views.History)
    app.router.add_view("/last_statuses", views.LastStatuses)
    app.router.add_view("/interval", views.Interval)
    #debug
    app.router.add_get("/clear", views.ClearAllTables)