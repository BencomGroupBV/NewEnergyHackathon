namespace NewEnergyHackathon.Web.Models;

public class EnergyMixDataWrapper
{
  public List<EnergyMixEntry> Data { get; set; }

  public double DailyGreenScoreGrid { get; set; }
}

public class EnergyMixEntry
{
  public DateTime Validfrom { get; set; }
  public double Volume_Solar { get; set; }
  public double Volume_Wind { get; set; }
  public double Volume_TotalMix { get; set; }
  public double Solar_Percentage { get; set; }
  public double Wind_Percentage { get; set; }
  public double TotalGreen_Percentage { get; set; }
}