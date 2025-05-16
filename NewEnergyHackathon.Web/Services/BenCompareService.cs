namespace NewEnergyHackathon.Web.Services;

public interface IBenCompareService
{
  string GetBencompareData();
}

public class BenCompareService : IBenCompareService
{
  public string GetBencompareData()
  {
    var dataFilePath = Path.Combine(AppContext.BaseDirectory, "user-smartmeter-data-no-solar-pannels.json");
    var bencompareUsageData = File.ReadAllText(dataFilePath);

    return bencompareUsageData;
  }
}
