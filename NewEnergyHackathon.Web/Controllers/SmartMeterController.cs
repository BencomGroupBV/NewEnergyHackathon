using Microsoft.AspNetCore.Mvc;
using NewEnergyHackathon.Web.Services;

namespace NewEnergyHackathon.Web.Controllers;

[ApiController]
public class SmartMeterController(ISmartMeterService smartMeterService) : Controller
{
  [HttpGet("smartmeterdata")]
  public IActionResult Index()
  {
    var userData = smartMeterService.GetSmartMeterData();

    return Ok(userData);
  }
}
