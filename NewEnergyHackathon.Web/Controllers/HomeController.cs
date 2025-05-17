using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using NewEnergyHackathon.Web.Models;

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
    return View();
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

  public IActionResult GreenEnergyForecast(DateTime? before, DateTime? after)
  {
	// You can pass these values to the view via ViewBag, ViewData, or a ViewModel
	//ViewBag.BeforeDate = before?.ToString("yyyy-MM-dd");
	//ViewBag.AfterDate = after?.ToString("yyyy-MM-dd");

	return View();
  }

  public IActionResult Settings()
  {
    return View();
  }
}
