using Microsoft.AspNetCore.Mvc;

namespace NewEnergyHackathon.Web.Controllers;
public class HomeController : Controller
{
  private readonly ILogger<HomeController> _logger;

  public HomeController(ILogger<HomeController> logger)
  {
    _logger = logger;
  }

  public IActionResult Index()
  {
    return View("SmartMeterDataUsage");
  }

  public IActionResult SmartMeterDataUsage()
  {
    return View();
  }

  public IActionResult UserEnergyConsumption()
  {
    return View();
  }


  public IActionResult History()
  {
    return View();
  }

  public IActionResult GreenEnergyForecast()
  {
    return View();
  }

  public IActionResult Settings()
  {
    return View();
  }
}
