using Microsoft.AspNetCore.Mvc;
using NewEnergyHackathon.Web.Services;
using Python.Runtime;

namespace NewEnergyHackathon.Web.Controllers;

[ApiController]
public class NedContoller(INedService nedService) : Controller
{
  [HttpGet("results")]
  public async Task<IActionResult> GetResults([FromQuery] int typeId, DateOnly before, DateOnly after)
  {
    var solar = await nedService.GetResultsAsync(2, before, after);
    var wind = await nedService.GetResultsAsync(1, before, after);
    var totalmix = await nedService.GetResultsAsync(27, before, after);

    PythonEngine.Initialize();

    using (Py.GIL())
    {
      dynamic sys = Py.Import("sys");
      sys.path.append(".");

      dynamic calc = Py.Import("datawrangling");

      try
      {
        string resultJson = calc.percentageNEDGreenEnergySingleDay(solar, wind, totalmix, "2025-05-16").ToString();
      }
      catch (Exception e)
      {
        Console.WriteLine(e);
        throw;
      }
      
      return Ok();
    }
  }
}
