using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;
using NewEnergyHackathon.Web.Services;
using Python.Runtime;

namespace NewEnergyHackathon.Web.Controllers;

[ApiController]
public class NedContoller(INedService nedService, IBenCompareService benCompareService) : Controller
{
  [HttpGet("green-energy-forecast")]
  public async Task<IActionResult> GetResults([FromQuery] int typeId, DateOnly before, DateOnly after)
  {
    var solar = await nedService.GetGridConsumptionByEnergyType(2, before, after);
    var wind = await nedService.GetGridConsumptionByEnergyType(1, before, after);
    var totalmix = await nedService.GetGridConsumptionByEnergyType(27, before, after);

    PythonEngine.Initialize();

    using (Py.GIL())
    {
      dynamic sys = Py.Import("sys");
      sys.path.append(".");

      dynamic calc = Py.Import("datawrangling");
      var resultJson = calc.percentageNEDGreenEnergySingleDay(solar, wind, totalmix, "2025-03-22").ToString();
      
      return Ok(resultJson);
    }
  }



  [HttpGet("daily-grid-consumption")]
  public async Task<IActionResult> GetGridConsumption([FromQuery] int typeId, DateOnly before, DateOnly after)
  {
    var solar = await nedService.GetGridConsumptionByEnergyType(2, before, after);
    var wind = await nedService.GetGridConsumptionByEnergyType(1, before, after);
    var totalmix = await nedService.GetGridConsumptionByEnergyType(27, before, after);

    PythonEngine.Initialize();

    using (Py.GIL())
    {
      dynamic sys = Py.Import("sys");
      sys.path.append(".");

      dynamic calc = Py.Import("datawrangling");

      var bencompareData = benCompareService.GetBencompareData();
      var gridConsumptionResult = calc.greenBehaviourPercentagesSingleDaySingleNonSolarUser(bencompareData, solar, wind, totalmix, "2025-03-22").ToString();


      return Ok(gridConsumptionResult);
    }
  }
}
