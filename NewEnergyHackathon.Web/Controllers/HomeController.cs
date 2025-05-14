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

  public IActionResult Profile()
  {
    return View();
  }

  public IActionResult Settings()
  {
    return View();
  }
}
