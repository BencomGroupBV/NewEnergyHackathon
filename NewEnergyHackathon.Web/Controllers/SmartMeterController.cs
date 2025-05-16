using Microsoft.AspNetCore.Mvc;
using NewEnergyHackathon.Web.Services;

namespace NewEnergyHackathon.Web.Controllers;

[ApiController]
public class SmartMeterController(ISmartMeterService smartMeterService, IBenCompareService benCompareService) : Controller
{
  [HttpGet("smartmeterdata")]
  public IActionResult Index()
  {
    var userData = smartMeterService.GetSmartMeterData();

    return Ok(userData);
  }

  [HttpGet("smartmeterdata-no-solar-pannels")]
  public IActionResult BencompareUsage()
  {
    var date = "2025-03-22";

    var userData = benCompareService
      .GetBencompareData(date);

    return Ok(userData);
  }
}
