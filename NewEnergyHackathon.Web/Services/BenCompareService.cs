using NewEnergyHackathon.Web.Models;
using System.Text.Json;

namespace NewEnergyHackathon.Web.Services;

public interface IBenCompareService
{
  string GetBencompareData(string date);
}

public class BenCompareService : IBenCompareService
{
  public string GetBencompareData(string date)
  {
    var dataFilePath = Path.Combine(AppContext.BaseDirectory, "user-smartmeter-data-no-solar-pannels.json");
    var bencompareUsageData = File.ReadAllText(dataFilePath);
    var bencompareModel = JsonSerializer.Deserialize<List<BencompareUsage>>(bencompareUsageData);

    var filtered = bencompareModel
      .Where(x => x.ItemsTimestampUTCDate == date)
      .ToList();

    return JsonSerializer.Serialize(filtered);
  }
}
