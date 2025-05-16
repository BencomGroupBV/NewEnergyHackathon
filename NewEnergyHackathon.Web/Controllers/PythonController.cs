using Microsoft.AspNetCore.Mvc;
using Python.Runtime;
using System.Text.Json;

namespace NewEnergyHackathon.Web.Controllers
{
  public class PythonController : Controller
  {
	public static CalculationRequest Example => new()
	{
	  DailyInputOfType = [4, 9, 16],
	  TotalMix = [5, 10, 16]
	};

	public class CalculationRequest
	{
	  public List<int> DailyInputOfType { get; set; }

	  public string DailyInputType { get; set; }

	  public List<int> TotalMix { get; set; }
	}

	// async calculate task
	public static async Task Calculator(CalculationRequest input)
	{
	  var jsonInput = JsonSerializer.Serialize(input);

	  PythonEngine.Initialize();
	  using (Py.GIL())
	  {
		dynamic sys = Py.Import("sys");
		sys.path.append(".");

		dynamic calc = Py.Import("calculation");
		string resultJson = calc.calculate(jsonInput).ToString();

		var result = JsonSerializer.Deserialize<Dictionary<string, object>>(resultJson);

		Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
	  }
	}
  }
}
