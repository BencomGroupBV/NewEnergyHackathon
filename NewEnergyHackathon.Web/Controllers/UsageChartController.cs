using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Memory;
using NewEnergyHackathon.Web.Models;
using NewEnergyHackathon.Web.Models.Enums;
using NewEnergyHackathon.Web.Services;
using Python.Runtime;

namespace NewEnergyHackathon.Web.Controllers;

[ApiController]
public class UsageChartController(INedService nedService, IBenCompareService benCompareService, IMemoryCache cache) : Controller
{
  private const string DateOfEnergyConsumption = "2025-03-22";

  [HttpGet("daily-green-energy")]
  public async Task<IActionResult> GetResults([FromQuery] DateOnly dateTo, DateOnly dateFrom)
  {

    if (!cache.TryGetValue("solar", out var solar))
    {
      solar = await nedService.GetGridConsumptionByEnergyType(EnergyType.Solar, dateTo, dateFrom);
      cache.Set("solar", solar);
    }

    if (!cache.TryGetValue("wind", out var wind))
    {
      wind = await nedService.GetGridConsumptionByEnergyType(EnergyType.Wind, dateTo, dateFrom);
      cache.Set("wind", wind);
    }

    if (!cache.TryGetValue("totalmix", out var totalmix))
    {
      totalmix = await nedService.GetGridConsumptionByEnergyType(EnergyType.ElectricityMix, dateTo, dateFrom);
      cache.Set("totalmix", totalmix);
    }

    using (Py.GIL())
    {
      dynamic sys = Py.Import("sys");
      sys.path.append(".");

      dynamic pythonCalculationFile = Py.Import("datawrangling");

      var dailyGreenEnergyGrid = pythonCalculationFile
        .percentageNEDGreenEnergySingleDay(solar, wind, totalmix, DateOfEnergyConsumption);

      var rawjson = dailyGreenEnergyGrid[0].ToString();
      var gridGreenScore = (double)dailyGreenEnergyGrid[1];

      var gridData = JsonSerializer.Deserialize<List<EnergyMixEntry>>(rawjson);

      var energyMixModel = new EnergyMixDataWrapper
      {
        Data = gridData,
        DailyGreenScoreGrid = gridGreenScore
      };

  

      return Ok(energyMixModel);
    }
  }

  [HttpGet("daily-green-consumption")]
  public async Task<IActionResult> GetGridConsumption([FromQuery] DateOnly dateTo, DateOnly dateFrom)
  {
    if (!cache.TryGetValue("solar", out var solar))
    {
      solar = await nedService.GetGridConsumptionByEnergyType(EnergyType.Solar, dateTo, dateFrom);
      cache.Set("solar", solar);
    }

    if (!cache.TryGetValue("wind", out var wind))
    {
      wind = await nedService.GetGridConsumptionByEnergyType(EnergyType.Wind, dateTo, dateFrom);
      cache.Set("wind", wind);
    }

    if (!cache.TryGetValue("totalmix", out var totalmix))
    {
      totalmix = await nedService.GetGridConsumptionByEnergyType(EnergyType.ElectricityMix, dateTo, dateFrom);
      cache.Set("totalmix", totalmix);
    }

    using (Py.GIL())
    {
      dynamic sys = Py.Import("sys");
      sys.path.append(".");

      dynamic pythonCalculationFile = Py.Import("datawrangling");

      var bencompareData = benCompareService.GetBencompareData(DateOfEnergyConsumption);

      var result = pythonCalculationFile.greenBehaviourPercentagesSingleDaySingleNonSolarUser(
        bencompareData,
        solar,
        wind,
        totalmix,
        DateOfEnergyConsumption
      );

      var rawJson = result[0];
      var userGreenScore = (double)result[1];
      var gridGreenScore = (double)result[2];

      var userScoreList = JsonSerializer.Deserialize<List<UserScoreData>>(rawJson);
      
      var bencompareModel = new UserScoreWrapper
      {
        Data = userScoreList,
        PercentageOfUserDailyGreenConsumption = userGreenScore,
        PercentageOfGridDailyGreenConsumption = gridGreenScore
      };

      return Ok(bencompareModel);
    }
  }
}
