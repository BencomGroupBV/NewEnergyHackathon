using NewEnergyHackathon.Web.Models;
using System.Text.Json;

namespace NewEnergyHackathon.Web.Services;

public interface IBenCompareService
{
  List<BencompareUsage> GetBencompareData();
}

public class BenCompareService : IBenCompareService
{
  public List<BencompareUsage> GetBencompareData()
  {
    var path = Path.Combine(AppContext.BaseDirectory, "user-smartmeter-data-no-solar-pannels.json");
    var json = File.ReadAllText(path);

    var options = new JsonSerializerOptions
    {
      PropertyNameCaseInsensitive = true
    };

    var readings = JsonSerializer.Deserialize<List<BencompareUsage>>(json, options);

    return readings;
  }
}
