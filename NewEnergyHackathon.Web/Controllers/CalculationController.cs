using Python.Runtime;
using System.Text.Json;

namespace NewEnergyHackathon.Web.Controllers
{
  public class CalculationController
  {
	public class CalculationRequest
	{
	  public List<int> Values { get; set; } = [4, 9, 16];
	}

	// async calculate task
	public static async Task PythonCalculate(CalculationRequest input)
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
