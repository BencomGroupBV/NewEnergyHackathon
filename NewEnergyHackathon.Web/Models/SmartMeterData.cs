namespace NewEnergyHackathon.Web.Models;

public class SmartMeterData
{
  public string EntityId { get; set; }
  public string Type { get; set; }
  public string Unit { get; set; }

  public Dictionary<string, double> TimeSeries { get; set; }
}
