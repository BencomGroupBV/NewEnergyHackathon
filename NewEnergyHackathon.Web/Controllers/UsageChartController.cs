using Microsoft.AspNetCore.Mvc;
using NewEnergyHackathon.Web.Models.Enums;
using NewEnergyHackathon.Web.Services;
using Python.Runtime;

namespace NewEnergyHackathon.Web.Controllers;

[ApiController]
public class UsageChartController(INedService nedService, IBenCompareService benCompareService) : Controller
{
  private const string DateOfEnergyConsumption = "2025-03-22";

  [HttpGet("daily-green-energy")]
  public async Task<IActionResult> GetResults([FromQuery] DateOnly dateTo, DateOnly dateFrom)
  {
    var solar = await nedService.GetGridConsumptionByEnergyType(EnergyType.Solar, dateTo, dateFrom);
    var wind = await nedService.GetGridConsumptionByEnergyType(EnergyType.Wind, dateTo, dateFrom);
    var totalmix = await nedService.GetGridConsumptionByEnergyType(EnergyType.ElectricityMix, dateTo, dateFrom);

    PythonEngine.Initialize();

    using (Py.GIL())
    {
      dynamic sys = Py.Import("sys");
      sys.path.append(".");

      dynamic pythonCalculationFile = Py.Import("datawrangling");

      var dailyGreenEnergyGrid = pythonCalculationFile
        .percentageNEDGreenEnergySingleDay(solar, wind, totalmix, DateOfEnergyConsumption).ToString();
      
      return Ok(dailyGreenEnergyGrid);
    }
  }

  [HttpGet("daily-green-consumption")]
  public async Task<IActionResult> GetGridConsumption([FromQuery] DateOnly dateTo, DateOnly dateFrom)
  {
    var solar = await nedService.GetGridConsumptionByEnergyType(EnergyType.Solar, dateTo, dateFrom);
    var wind = await nedService.GetGridConsumptionByEnergyType(EnergyType.Wind, dateTo, dateFrom);
    var totalmix = await nedService.GetGridConsumptionByEnergyType(EnergyType.ElectricityMix, dateTo, dateFrom);

    PythonEngine.Initialize();

    using (Py.GIL())
    {
      dynamic sys = Py.Import("sys");
      sys.path.append(".");

      dynamic pythonCalculationFile = Py.Import("datawrangling");

      var bencompareData = benCompareService.GetBencompareData(DateOfEnergyConsumption);

      var dailyGreenPercentageScores = pythonCalculationFile
        .greenBehaviourPercentagesSingleDaySingleNonSolarUser(bencompareData, solar, wind, totalmix, DateOfEnergyConsumption).ToString();

      return Ok(dailyGreenPercentageScores);
    }
  }
}
