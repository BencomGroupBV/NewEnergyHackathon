using System.Text.Json;
using NewEnergyHackathon.Web.Models;

namespace NewEnergyHackathon.Web.Services;

public interface ISmartMeterService
{
  List<SmartMeterData> GetSmartMeterData();
}

public class SmartMeterService : ISmartMeterService
{
  public List<SmartMeterData> GetSmartMeterData()
  {
    var path = Path.Combine(AppContext.BaseDirectory, "user-smart-meter-data.json");
    var json = File.ReadAllText(path);

    var rawList = JsonSerializer.Deserialize<List<Dictionary<string, JsonElement>>>(json);

    var readings = rawList.Select(raw =>
    {
      var reading = new SmartMeterData
      {
        EntityId = raw["entity_id"].GetString(),
        Type = raw["type"].GetString(),
        Unit = raw["unit"].GetString(),
        TimeSeries = raw
          .Where(kvp => kvp.Key != "entity_id" && kvp.Key != "type" && kvp.Key != "unit")
          .ToDictionary(kvp => kvp.Key, kvp => kvp.Value.GetDouble())
      };
      return reading;
    }).ToList();

    return readings;
  }
}
