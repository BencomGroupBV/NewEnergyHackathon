using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using Python.Runtime;

namespace NewEnergyHackathon.Web.Controllers
{
  public class PythonController : Controller
  {
    public static CalculationRequest Example => new()
    {
      DailyInputOfType = [4, 9, 16],
      TotalMix = [5, 10, 16]
    };


    [HttpGet("calculate-green")]
    public IActionResult GetGreenEnergyMix()
    {
      var request = new CalculationRequest
      {
        DailyInputOfType = [4, 9, 16],
        TotalMix = [5, 10, 16]
      };

      var input = JsonSerializer.Serialize(request);

      PythonEngine.Initialize();

      using (Py.GIL())
      {
        dynamic sys = Py.Import("sys");
        sys.path.append(".");

        dynamic calc = Py.Import("datawrangling");


        string resultJson = calc.percentageNEDGreenEnergySingleDay(input).ToString();

        var result = JsonSerializer.Deserialize<Dictionary<string, object>>(resultJson);

        return Ok(JsonSerializer.Serialize(result));
      }
    }


    public class CalculationRequest
    {
      public List<int> DailyInputOfType { get; set; }

      public string DailyInputType { get; set; }

      public List<int> TotalMix { get; set; }
    }

    }
  }
