resource "azurerm_linux_web_app" "webapp" {
  name                = "paulolabfrontend"
  location            = var.location
  resource_group_name = var.resource_group_name
  service_plan_id     = azurerm_service_plan.lab_appservice.id

  site_config {
    python_version     = "3.10"
    app_command_line   = "gunicorn -w 2 -b 0.0.0.0:8000 app:app"
    health_check_path  = "/health"
  }

  app_settings = {
    "WEBSITES_PORT" = "8000"
  }  

  depends_on = [
    azurerm_service_plan.lab_appservice
  ]
}
